#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
sleep 10

# Run database migrations and seed data
python -m app.init_data.seed

# Start the FastAPI application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000