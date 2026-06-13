# ============================================================================
# FraudShield AI - Docker Container Configuration
# ============================================================================
# Build and deploy the fraud detection dashboard in a container

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY config.py .
COPY components.py .
COPY utils.py .
COPY README.md .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DASH_DEBUG=False

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8050')" || exit 1

# Run the application
CMD ["gunicorn", "--workers=4", "--threads=2", "--worker-class=gthread", \
     "--worker-connections=1000", "--timeout=60", "--bind=0.0.0.0:8050", \
     "--access-logfile=-", "--error-logfile=-", "app:server"]
