# ------------------------------------------------------------------------------
# File Name: ssh_config_checks.py
# Project: SSH Config Auditor
# Author: _01x.arec1b0(dkrizhanovskyi)
# License: MIT
# Last Updated: 2024-12-25
# Description:
#   Contains the SSHConfigAuditor class, which connects to a remote SSH server,
#   retrieves sshd_config, and evaluates security-critical directives.
# ------------------------------------------------------------------------------

"""
ssh_config_checks.py

Implements the SSHConfigAuditor class using Paramiko to connect, retrieve, and
evaluate an SSH server’s configuration (e.g., password auth, port, root login).
"""

import paramiko
from auditor.utils.parser import (
    parse_sshd_config,
    validate_ssh_port,
    normalize_boolean_setting
)


class SSHConfigAuditor:
    """
    Audits SSH server configurations for security best practices.
    """

    def __init__(
        self,
        host: str,
        username: str,
        port: int = 22,
        password: str | None = None,
        key_file: str | None = None
    ) -> None:
        """
        Initializes SSHConfigAuditor with connection details.

        Args:
            host (str): Target server's hostname or IP address.
            username (str): SSH username.
            port (int, optional): SSH port (default 22).
            password (str | None, optional): SSH password (default None).
            key_file (str | None, optional): Path to an SSH private key (default None).
        """
        self.host = host
        self.username = username
        self.port = port
        self.password = password
        self.key_file = key_file

    def audit_ssh_config(self) -> dict[str, str]:
        """
        Establishes an SSH connection, retrieves sshd_config, and performs audits.

        Returns:
            dict[str, str]: Results keyed by configuration directive name.
        """
        results = {}
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect with password or key
            if self.password:
                client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=5
                )
            else:
                key = None
                if self.key_file:
                    key = paramiko.RSAKey.from_private_key_file(self.key_file)
                client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.username,
                    pkey=key,
                    timeout=5
                )

            # Retrieve sshd_config
            sftp = client.open_sftp()
            try:
                with sftp.open("/etc/ssh/sshd_config", "r") as remote_file:
                    config_data = remote_file.read().decode("utf-8")
            except IOError:
                config_data = ""
            finally:
                sftp.close()

            if config_data:
                config_dict = parse_sshd_config(config_data)
                results["PortConfig"] = self.check_port(config_dict)
                results["PasswordAuthentication"] = self.check_password_auth(config_dict)
                results["RootLogin"] = self.check_root_login(config_dict)
            else:
                results["Error"] = "Unable to retrieve sshd_config."

        except paramiko.SSHException as ssh_err:
            results["ConnectionError"] = f"SSH error: {ssh_err}"
        finally:
            client.close()

        return results

    @staticmethod
    def check_port(config_dict: dict[str, str]) -> str:
        """
        Checks if the SSH server uses a non-default port (not 22).

        Args:
            config_dict (dict[str, str]): Parsed sshd_config key-value pairs.

        Returns:
            str: "Secure (Port XYZ)" if non-default, otherwise "Default (Port 22)".
        """
        port = config_dict.get("Port", "22")
        if validate_ssh_port(port) and port != "22":
            return f"Secure (Port {port})"
        return "Default (Port 22)"

    @staticmethod
    def check_password_auth(config_dict: dict[str, str]) -> str:
        """
        Determines if PasswordAuthentication is disabled (secure).

        Args:
            config_dict (dict[str, str]): Parsed sshd_config.

        Returns:
            str: "Secure" if no, "Insecure" if yes, or "Unknown" if not found.
        """
        value = config_dict.get("PasswordAuthentication", "yes")
        normalized = normalize_boolean_setting(value)
        if normalized is False:
            return "Secure"
        elif normalized is True:
            return "Insecure"
        return "Unknown"

    @staticmethod
    def check_root_login(config_dict: dict[str, str]) -> str:
        """
        Evaluates if PermitRootLogin is disabled or restricted.

        Args:
            config_dict (dict[str, str]): Parsed sshd_config.

        Returns:
            str: "Secure" if no/without-password/prohibit-password,
                 "Insecure" if yes, or "Unknown" otherwise.
        """
        value = config_dict.get("PermitRootLogin", "yes").lower()
        if value in ["no", "without-password", "prohibit-password"]:
            return "Secure"
        elif value == "yes":
            return "Insecure"
        return "Unknown"


# ------------------------------------------------------------------------------
# Footer Notes:
# - Ensure that the user running Paramiko has necessary permissions
#   to read /etc/ssh/sshd_config.
# - MIT License applies.
# ------------------------------------------------------------------------------

