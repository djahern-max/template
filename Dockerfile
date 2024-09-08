# Use the python 3.12-slim image
FROM python:3.12-slim

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

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




