"""
api.py - FastAPI implementation for SSH Config Auditor.
Adheres to SOLID principles by separating HTTP logic from auditing logic.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auditor.checks.ssh_config_checks import SSHConfigAuditor

app = FastAPI(title="SSH Config Auditor API", version="1.0.0")


class AuditRequest(BaseModel):
    host: str
    username: str = "root"
    port: int = 22
    password: str | None = None
    key_file: str | None = None


@app.post("/audit")
def audit_ssh_config(request: AuditRequest):
    """
    POST /audit endpoint:
    - Accepts SSH details (host, port, etc.).
    - Performs an audit using SSHConfigAuditor.
    - Returns a JSON response with results.
    """
    auditor = SSHConfigAuditor(
        host=request.host,
        username=request.username,
        port=request.port,
        password=request.password,
        key_file=request.key_file,
    )
    try:
        results = auditor.audit_ssh_config()
        return {"status": "OK", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

