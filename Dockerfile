# Use Python 3.10 slim image as base for smaller image size
FROM python:3.10-slim

# Set Python environment variables for production optimization
# PYTHONDONTWRITEBYTECODE: Prevents creation of .pyc files (reduces image size)
# PYTHONUNBUFFERED: Ensures Python output is sent directly to terminal (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1 \
   PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and build tools
# - Update package lists and upgrade existing packages
# - Install gcc, python3-dev, and libssl-dev for building Python packages
# - Remove apt cache to reduce image size
# - Upgrade pip, setuptools, and wheel to latest versions
# - Create a non-root user for security (appuser/appgroup)
RUN apt-get update && \
   apt-get upgrade -y && \
   apt-get install -y --no-install-recommends gcc python3-dev libssl-dev && \
   rm -rf /var/lib/apt/lists/* && \
   python -m pip install --upgrade pip setuptools>=70.0.0 wheel && \
   groupadd -r appgroup && \
   useradd -r -g appgroup appuser

# Copy requirements file first for better Docker layer caching
# This allows Docker to cache the pip install step if requirements don't change
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir: Don't store downloaded packages (reduces image size)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Change ownership of /app directory to appuser for security
# This ensures the application runs with proper permissions
RUN chown -R appuser:appgroup /app

# Switch to non-root user for security
# This follows the principle of least privilege - if the container is compromised,
# the attacker has limited permissions
USER appuser

# Health check configuration
# - Checks every 30 seconds if the application is healthy
# - Waits 5 seconds for app to start before first check
# - Timeout of 30 seconds per check
# - Retry up to 3 times before marking as unhealthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
   CMD curl -f http://localhost:8000/health || exit 1

# Start the FastAPI application using Uvicorn ASGI server
# - main:app: Points to the app instance in main.py
# - --host 0.0.0.0: Listen on all network interfaces
# - --port 8000: Expose the application on port 8000
# - --workers 4: Use 4 worker processes for better performance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]