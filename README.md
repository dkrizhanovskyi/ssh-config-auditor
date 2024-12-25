# **SSH Config Auditor**

A Python-based auditor that inspects SSH server configurations for security best practices. This tool checks parameters like **PasswordAuthentication**, **PermitRootLogin**, and **Port** settings to ensure a hardened setup. It can be used both as a **CLI** tool and a **FastAPI** service.

---

## **Table of Contents**
1. [Features](#features)  
2. [Architecture Overview](#architecture-overview)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
   - [CLI Usage](#cli-usage)  
   - [FastAPI Usage](#fastapi-usage)  
6. [Testing](#testing)  
7. [Docker / Podman](#docker--podman)  
8. [Security Considerations](#security-considerations)  
9. [Contributing](#contributing)

---

## **Features**
- **CLI Interface** for local or automated audits.
- **FastAPI Web Interface** for initiating and reviewing audits via REST API.
- **Paramiko** integration to securely connect and fetch SSH configurations.
- **Modular Architecture** to add or remove checks easily.
- **Optional PDF Reporting** for audit documentation (via ReportLab).
- **Unit Tests** with pytest to ensure robust functionality.

---

## **Architecture Overview**

```bash
ssh-config-auditor
├── auditor
│   ├── api.py        # FastAPI endpoints
│   ├── checks        # SSH checks (ssh_config_checks.py)
│   ├── main.py       # CLI entry point
│   ├── reports       # Optional PDF reporting
│   └── utils         # Parsing utilities, helpers
├── tests             # Pytest-based tests
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container build file
└── README.md
```

**Key Modules**:

- **checks/**: Contains the core SSH auditing logic in `ssh_config_checks.py`.  
- **main.py**: Primary CLI entry point, handling user inputs and orchestrating checks.  
- **api.py**: FastAPI application for REST-based interactions.  
- **reports/**: PDF and other reporting modules.  

---

## **Prerequisites**

1. **Python 3.9+**  
2. **pip** (Python package manager)  
3. **(Optional)** **Docker / Podman** for containerized deployment

On Fedora or other Linux distributions, ensure you have basic build tools if using cryptography libraries:

```bash
sudo dnf install gcc openssl-devel libffi-devel
```

---

## **Installation**

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/dkrizhanovskyi/ssh-config-auditor.git
   cd ssh-config-auditor
   ```

   Or via SSH:

   ```bash
   git clone git@github.com:dkrizhanovskyi/ssh-config-auditor.git
   cd ssh-config-auditor
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## **Usage**

### **CLI Usage**
Run the CLI directly via the `main.py` script:
```bash
python auditor/main.py --host 192.168.1.10 \
                       --user root \
                       --port 22 \
                       --password SECRET
```

**Arguments**:
- `--host` (required): Target SSH server IP or hostname.  
- `--user` (default: `root`): SSH username.  
- `--port` (default: `22`): SSH port.  
- `--key` (optional): Path to a private key for key-based auth.  
- `--password` (optional): SSH password if not using key-based auth.

### **FastAPI Usage**
1. **Launch** the FastAPI service:
   ```bash
   uvicorn auditor.api:app --host 0.0.0.0 --port 8000
   ```
2. **Open** a browser at:
   ```
   http://127.0.0.1:8000/docs
   ```
3. **Invoke** the `/audit` endpoint with a JSON payload specifying `host`, `username`, etc.

---

## **Testing**
Use **pytest** for running unit tests:

1. **Activate** your virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. **Execute** the tests:
   ```bash
   pytest --maxfail=1 --disable-warnings
   ```
3. **(Optional)** Test coverage:
   ```bash
   pip install pytest-cov
   pytest --cov=auditor tests/
   ```

---

## **Docker / Podman**

### **Build the Image**
```bash
podman build -t ssh-config-auditor:latest .
```
Or if you prefer Docker:
```bash
docker build -t ssh-config-auditor:latest .
```

### **Run the Container**
```bash
podman run -p 8000:8000 \
           --name auditor \
           -d ssh-config-auditor:latest
```

If you see an error about an existing container, remove or replace it:
```bash
podman rm -f auditor
podman run --replace -p 8000:8000 \
           --name auditor \
           -d ssh-config-auditor:latest
```

Access the FastAPI docs at:  
```
http://127.0.0.1:8000/docs
```

---

## **Security Considerations**
- **SSH Keys**: Avoid storing private keys in plain text or in the repo; use environment variables or secret managers (e.g., HashiCorp Vault).  
- **Logging**: Consider signing logs or storing them in an append-only system for tamper resistance.  
- **API Authentication**: Secure exposed endpoints with token-based auth or BasicAuth if deploying publicly.  
- **Least Privilege**: Limit the SSH user to read-only permissions for `/etc/ssh/sshd_config`.  

---

## **Contributing**
1. **Fork** the project & create a feature branch from `develop`.  
2. **Implement** your changes, adding relevant tests.  
3. **Commit** with descriptive messages.  
4. **Open** a pull request towards `develop`.  
5. **Ensure** all tests and lint checks pass before merging.

For major features or design changes, please open an issue to discuss them first!

---

**Thank you for using SSH Config Auditor!**  

