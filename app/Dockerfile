# Use an official Python runtime as the base image
FROM python:3.9-slim

# Author
LABEL authors="uddiptapoddar"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Make the migration script executable
RUN chmod +x run_migrations.sh

# Expose the port on which the application will run
EXPOSE 8000

# Run migrations and start the FastAPI application
CMD ["sh", "-c", "./run_migrations.sh && uvicorn main:app --host 0.0.0.0 --port 8000"]
