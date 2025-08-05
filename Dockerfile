FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxrandr2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install basic packages first
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies in stages
COPY requirements.txt .

# Install core dependencies first
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
RUN pip install --no-cache-dir \
    diffusers>=0.21.0 \
    transformers>=4.30.0 \
    accelerate>=0.20.0 \
    safetensors>=0.3.0 \
    Pillow>=10.0.0 \
    numpy>=1.24.0 \
    opencv-python-headless>=4.8.0 \
    flask>=2.3.0 \
    requests>=2.31.0 \
    runpod>=1.5.0

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
