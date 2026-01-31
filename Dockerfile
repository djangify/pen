FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies including gosu for dropping privileges
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  gosu \
  && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . /app/

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Required directories
RUN mkdir -p /app/media /app/db /app/logs /app/staticfiles

# Non-root user (created but not switched to - entrypoint handles this)
RUN useradd -m appuser && chown -R appuser:appuser /app

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]