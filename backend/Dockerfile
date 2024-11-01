FROM python:3.11-slim

WORKDIR /backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /backend/logs

# Make the startup script executable
COPY startup.sh .
RUN chmod +x startup.sh

# Run migrations and seed data on startup
CMD ["./startup.sh"]