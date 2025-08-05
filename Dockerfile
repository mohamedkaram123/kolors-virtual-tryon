FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /app

# Install essential packages for image processing
RUN pip install --no-cache-dir runpod Pillow

# Copy only the essential handler
COPY handler_ultra.py handler.py

# Set environment
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Start handler
CMD ["python", "handler.py"]