FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (for paramiko, cryptography)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev sshpass \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "auditor.api:app", "--host", "0.0.0.0", "--port", "8000"]

