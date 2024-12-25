"""
ssh_config_checks.py - Contains the SSHConfigAuditor class, which uses parser utilities
to audit SSH configurations for security best practices.
"""

from auditor.utils.parser import (
    parse_sshd_config,
    validate_ssh_port,
    normalize_boolean_setting
)
import paramiko


class SSHConfigAuditor:
    """
    SSHConfigAuditor class to audit SSH server configurations for compliance
    with security best practices.
    """

    def __init__(self, host, username, port=22, password=None, key_file=None):
        self.host = host
        self.username = username
        self.port = port
        self.password = password
        self.key_file = key_file

    def audit_ssh_config(self):
        """
        Orchestrates the SSH configuration audit:
        - Establishes an SSH connection.
        - Retrieves sshd_config.
        - Performs security checks.

        Returns:
            dict: Audit results.
        """
        results = {}
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the SSH server
            if self.password:
                client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=5
                )
            else:
                key = paramiko.RSAKey.from_private_key_file(self.key_file) if self.key_file else None
                client.connect(
                    self.host,
                    port=self.port,
                    username=self.username,
                    pkey=key,
                    timeout=5
                )

            # Retrieve sshd_config file
            sftp = client.open_sftp()
            try:
                with sftp.open("/etc/ssh/sshd_config", "r") as remote_file:
                    config_data = remote_file.read().decode("utf-8")
            except IOError:
                config_data = ""  # If sshd_config isn't accessible
            finally:
                sftp.close()

            # Parse and analyze the configuration
            if config_data:
                config_dict = parse_sshd_config(config_data)
                results["PortConfig"] = self.check_port(config_dict)
                results["PasswordAuthentication"] = self.check_password_auth(config_dict)
                results["RootLogin"] = self.check_root_login(config_dict)
            else:
                results["Error"] = "Unable to retrieve sshd_config."

        except paramiko.SSHException as e:
            results["ConnectionError"] = str(e)
        finally:
            client.close()

        return results

    @staticmethod
    def check_port(config_dict):
        """
        Checks if the SSH server is using a non-default port (not 22).

        Args:
            config_dict (dict): Parsed sshd_config settings.

        Returns:
            str: 'Secure' for non-default ports, 'Default' otherwise.
        """
        port = config_dict.get("Port", "22")
        if validate_ssh_port(port) and port != "22":
            return f"Secure (Port {port})"
        return "Default (Port 22)"

    @staticmethod
    def check_password_auth(config_dict):
        """
        Checks if PasswordAuthentication is disabled.

        Args:
            config_dict (dict): Parsed sshd_config settings.

        Returns:
            str: 'Secure' if disabled, 'Insecure' otherwise.
        """
        value = config_dict.get("PasswordAuthentication", "yes")
        normalized = normalize_boolean_setting(value)
        if normalized is False:
            return "Secure"
        elif normalized is True:
            return "Insecure"
        return "Unknown"

    @staticmethod
    def check_root_login(config_dict):
        """
        Checks if root login is disabled.

        Args:
            config_dict (dict): Parsed sshd_config settings.

        Returns:
            str: 'Secure' if disabled, 'Insecure' otherwise.
        """
        value = config_dict.get("PermitRootLogin", "yes")
        normalized = normalize_boolean_setting(value)
        if normalized is False:
            return "Secure"
        elif normalized is True:
            return "Insecure"
        return "Unknown"

