# ------------------------------------------------------------------------------
# File Name: api.py
# Project: SSH Config Auditor
# Author: _01x.arec1b0(dkrizhanovskyi)
# License: MIT
# Last Updated: 2024-12-25
# Description:
#   Exposes the SSH configuration audit functionality over a FastAPI REST API.
# ------------------------------------------------------------------------------

"""
api.py

Defines a FastAPI application to perform SSH config audits via an HTTP/JSON API.
Relies on SSHConfigAuditor from ssh_config_checks.py for the core checks.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auditor.checks.ssh_config_checks import SSHConfigAuditor

app = FastAPI(
    title="SSH Config Auditor API",
    version="1.0.0",
    description=(
        "A REST API to audit SSH configurations for security best practices. "
        "Uses Paramiko to connect and retrieve sshd_config settings."
    )
)


class AuditRequest(BaseModel):
    """
    Request payload for initiating an SSH audit via FastAPI.
    """
    host: str
    username: str = "root"
    port: int = 22
    password: str | None = None
    key_file: str | None = None


@app.post("/audit")
def audit_ssh_config(request: AuditRequest) -> dict:
    """
    Audits the SSH configuration of a specified host.

    Args:
        request (AuditRequest): Contains host, port, and optional credentials.

    Returns:
        dict: JSON-friendly object with the audit results.

    Raises:
        HTTPException: Returns a 500 if the audit process fails.
    """
    auditor = SSHConfigAuditor(
        host=request.host,
        username=request.username,
        port=request.port,
        password=request.password,
        key_file=request.key_file
    )
    try:
        results = auditor.audit_ssh_config()
        return {"status": "OK", "results": results}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ------------------------------------------------------------------------------
# Footer Notes:
# - To deploy publicly, add authentication or IP allowlisting to secure the API.
# - Logs may contain sensitive SSH details; handle them securely.
# - MIT License applies.
# ------------------------------------------------------------------------------

