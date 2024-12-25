"""
main.py - Entry point for SSH Config Auditor (CLI).
Adheres to SOLID principles by delegating checks and utilities
to dedicated modules like ssh_config_checks.py and parser.py.
"""

import argparse
from auditor.checks.ssh_config_checks import SSHConfigAuditor


def parse_arguments():
    """
    Parse CLI arguments.
    SRP: This function handles argument parsing only.
    """
    parser = argparse.ArgumentParser(description="SSH Config Auditor (CLI)")
    parser.add_argument("--host", required=True, help="Target SSH server IP or hostname")
    parser.add_argument("--user", default="root", help="SSH username")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("--password", default=None, help="SSH password (optional)")
    parser.add_argument("--key", default=None, help="Path to private key (optional)")
    return parser.parse_args()


def run_audit():
    """
    Orchestrates the SSH configuration audit via CLI.
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

