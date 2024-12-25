# ------------------------------------------------------------------------------
# File Name: parser.py
# Project: SSH Config Auditor
# Author: _01x.arec1b0(dkrizhanovskyi)
# License: MIT
# Last Updated: 2024-12-25
# Description:
#   Utility functions for parsing and validating sshd_config lines.
# ------------------------------------------------------------------------------

"""
parser.py

Provides a set of utility functions to parse sshd_config content into a usable
dictionary, as well as other helpers for validating or normalizing settings.
"""

import re

def parse_sshd_config(config_data: str) -> dict[str, str]:
    """
    Converts raw sshd_config text into a dictionary of key-value pairs.

    Args:
        config_data (str): The raw contents of sshd_config.

    Returns:
        dict[str, str]: A dictionary of directives (keys) to their values.
    """
    pattern = r"^\s*([A-Za-z0-9]+)\s+(.*)$"
    config_dict = {}
    for line in config_data.split("\n"):
        match = re.search(pattern, line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            config_dict[key] = value
    return config_dict


def validate_ssh_port(port: str) -> bool:
    """
    Checks if the given port string is a valid TCP port (1-65535).

    Args:
        port (str): The port value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False


def normalize_boolean_setting(value: str) -> bool | None:
    """
    Converts 'yes'/ 'no' / 'on' / 'off' strings to Python booleans.

    Args:
        value (str): e.g., 'yes', 'no', 'on', 'off'.

    Returns:
        bool | None: True if 'yes'/'on', False if 'no'/'off', None if unrecognized.
    """
    val_lower = value.strip().lower()
    if val_lower in ["yes", "on"]:
        return True
    elif val_lower in ["no", "off"]:
        return False
    return None

# ------------------------------------------------------------------------------
# Footer Notes:
# - These helpers serve as building blocks for advanced SSH config validations.
# - MIT License applies.
# ------------------------------------------------------------------------------

