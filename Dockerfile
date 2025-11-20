# Use a lightweight official Python base image
FROM python:3.12-slim

# ---------------------------------------------------------------
# Install system dependencies (including usbutils for lsusb)
# ---------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    usbutils \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------
# Set working directory
# ---------------------------------------------------------------
WORKDIR /app

# ---------------------------------------------------------------
# Copy dependency list and install Python packages
# ---------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------------------------------
# Copy the rest of the app into the container
# ---------------------------------------------------------------
COPY . .

# ---------------------------------------------------------------
# Expose the API port (FastAPI / Uvicorn default)
# ---------------------------------------------------------------
EXPOSE 8001

# ---------------------------------------------------------------
# Command to start FastAPI app
# ---------------------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


