"""
parser.py - Utility functions to parse and validate SSH configuration or other related data.
Part of the auditor.utils package.
"""

import re


def parse_sshd_config(config_data: str) -> dict:
    """
    Parse the sshd_config data and return a dictionary of relevant settings.
    
    :param config_data: Raw string of the sshd_config file contents
    :return: A dictionary mapping settings (keys) to their values
    """
    # Regex example for capturing key/value lines like 'Key Value'
    pattern = r'^\s*([A-Za-z0-9]+)\s+(.*)$'
    config_dict = {}
    for line in config_data.split('\n'):
        match = re.search(pattern, line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            config_dict[key] = value
    return config_dict


def validate_ssh_port(port: str) -> bool:
    """
    Validate that the SSH port is within the valid TCP port range (1-65535).
    
    :param port: Port value extracted from config_data
    :return: True if valid, False otherwise
    """
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False


def extract_config_value(config_dict: dict, key: str, default=None):
    """
    Safely retrieve a configuration value from a dictionary, returning a default if not found.
    
    :param config_dict: Dictionary of config key/value pairs
    :param key: The config key to retrieve
    :param default: Default value to return if key is not found
    :return: The requested value or the default
    """
    return config_dict.get(key, default)


def normalize_boolean_setting(value: str) -> bool | None:
    """
    Convert SSH config boolean values (yes/no/on/off) to Python booleans (True/False).
    
    :param value: String value representing a boolean in sshd_config
    :return: True/False, or None if unknown
    """
    if isinstance(value, str):
        val_lower = value.strip().lower()
        if val_lower in ["yes", "on"]:
            return True
        elif val_lower in ["no", "off"]:
            return False
    return None


if __name__ == "__main__":
    # Example usage:
    sample_config = """
    Port 22
    PasswordAuthentication yes
    PermitRootLogin no
    X11Forwarding yes
    """

    parsed = parse_sshd_config(sample_config)
    print("Parsed Config Dict:", parsed)

    port_valid = validate_ssh_port(parsed.get("Port", "22"))
    print(f"Is Port Valid? {port_valid}")

    root_login = normalize_boolean_setting(parsed.get("PermitRootLogin", "yes"))
    print(f"PermitRootLogin Setting: {root_login}")

