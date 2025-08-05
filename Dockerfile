FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone Kolors repository
RUN git clone https://github.com/Kwai-Kolors/Kolors.git /app/Kolors

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/uploads /app/outputs

# Set environment variables
ENV PYTHONPATH=/app:/app/Kolors
ENV TORCH_HOME=/app/models
ENV HF_HOME=/app/models

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "handler.py"]
