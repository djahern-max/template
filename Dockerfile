# Stage 1: Build stage for dependencies
FROM python:3.12-slim as builder

# Set the working directory
WORKDIR /user/src/app

# Install build tools, Rust, and Cargo (required for compiling certain Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    curl \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Rust to the PATH so that it's available during pip install
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy requirements.txt to the container
COPY requirements.txt ./ 

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.12-slim

# Set the working directory
WORKDIR /user/src/app

# Copy the virtual environment from the build stage
COPY --from=builder /opt/venv /opt/venv

# Ensure venv is active
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
COPY . .

# Create a non-root user
RUN adduser --disabled-password myuser
USER myuser

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




