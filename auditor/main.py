# ------------------------------------------------------------------------------
# File Name: main.py
# Project: SSH Config Auditor
# Author: _01x.arec1b0(dkrizhanovskyi)
# License: MIT
# Last Updated: 2024-12-25
# Description:
#   Provides a command-line interface (CLI) to run SSH configuration audits.
# ------------------------------------------------------------------------------

"""
main.py

Defines the entry point for a CLI-based SSH config auditing tool. It delegates
the core checks to ssh_config_checks.py and uses argparse for command-line args.
"""

import argparse
from auditor.checks.ssh_config_checks import SSHConfigAuditor


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the SSH Config Auditor.

    Returns:
        argparse.Namespace: Parsed args including host, user, port, password, key.
    """
    parser = argparse.ArgumentParser(
        description="SSH Config Auditor (CLI)",
        epilog="Example: python main.py --host 192.168.1.10 --port 22"
    )
    parser.add_argument("--host", required=True, help="Target SSH server IP/hostname.")
    parser.add_argument("--user", default="root", help="SSH username (default: root).")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22).")
    parser.add_argument("--password", default=None, help="SSH password (optional).")
    parser.add_argument("--key", default=None, help="Path to private SSH key (optional).")
    return parser.parse_args()


def run_audit() -> None:
    """
    Orchestrates the SSH configuration audit via the command line interface.

    1) Parses arguments.
    2) Instantiates SSHConfigAuditor.
    3) Prints results in a human-readable format.
    """
    args = parse_arguments()
    auditor = SSHConfigAuditor(
        host=args.host,
        username=args.user,
        port=args.port,
        password=args.password,
        key_file=args.key
    )
    results = auditor.audit_ssh_config()

    print("\n=== SSH Config Auditor Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    run_audit()

# ------------------------------------------------------------------------------
# Footer Notes:
# - Make sure to review logs carefully for any SSH errors.
# - All usage is subject to the MIT License.
# ------------------------------------------------------------------------------

