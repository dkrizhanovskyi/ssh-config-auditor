"""
test_ssh_config_checks.py - Unit tests for the SSHConfigAuditor class.
We’ll primarily test the static config parsing methods here.
"""

import pytest
from auditor.checks.ssh_config_checks import SSHConfigAuditor

def test_check_password_auth():
    """
    Verify that check_password_auth returns:
    - 'Secure' if PasswordAuthentication is no.
    - 'Insecure' if PasswordAuthentication is yes.
    - 'Unknown' if the setting is not found.
    """
    auditor = SSHConfigAuditor(host="127.0.0.1", username="testuser")

    # Pass dictionaries instead of raw strings
    config_data_secure = {"PasswordAuthentication": "no"}
    config_data_insecure = {"PasswordAuthentication": "yes"}
    config_data_none = {"PermitRootLogin": "no"}  # Missing 'PasswordAuthentication'

    assert auditor.check_password_auth(config_data_secure) == "Secure"
    assert auditor.check_password_auth(config_data_insecure) == "Insecure"
    assert auditor.check_password_auth(config_data_none) == "Unknown"


def test_check_root_login():
    """
    Verify that check_root_login returns:
    - 'Secure' for no/without-password/prohibit-password.
    - 'Insecure' otherwise.
    - 'Unknown' if the setting is not found.
    """
    auditor = SSHConfigAuditor(host="127.0.0.1", username="testuser")

    # Dictionaries with PermitRootLogin keys
    config_data_secure_no = {"PermitRootLogin": "no"}
    config_data_secure_prohibit = {"PermitRootLogin": "prohibit-password"}
    config_data_insecure = {"PermitRootLogin": "yes"}
    config_data_none = {"PasswordAuthentication": "no"}

    assert auditor.check_root_login(config_data_secure_no) == "Secure"
    assert auditor.check_root_login(config_data_secure_prohibit) == "Secure"
    assert auditor.check_root_login(config_data_insecure) == "Insecure"
    assert auditor.check_root_login(config_data_none) == "Unknown"


def test_check_port_config():
    """
    Verify that check_port_config returns a message for secure (non-default) ports
    or "Default (Port 22)" if none is found.
    """
    auditor = SSHConfigAuditor(host="127.0.0.1", username="testuser")

    config_data_custom_port = {"Port": "2222"}
    config_data_default = {}

    assert auditor.check_port(config_data_custom_port) == "Secure (Port 2222)"
    assert auditor.check_port(config_data_default) == "Default (Port 22)"

