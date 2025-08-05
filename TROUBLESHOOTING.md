# Troubleshooting Guide

## Docker Build Issues

### Problem: pip install fails during Docker build
**Error**: `process "/bin/bash -o pipefail -c pip install --no-cache-dir -r requirements.txt" did not complete successfully: exit code: 1`

**Solutions**:
1. **Use the updated Dockerfile** - The new version installs dependencies in stages
2. **Check internet connection** - Ensure Docker can download packages
3. **Increase Docker resources** - Allocate more RAM/disk space to Docker
4. **Use the deployment script**: `./deploy.sh your-registry latest`

### Problem: CUDA/GPU compatibility issues
**Solutions**:
1. Use the correct PyTorch CUDA version: `torch torchvision --index-url https://download.pytorch.org/whl/cu118`
2. Ensure RunPod instance has compatible GPU (A100, RTX 4090 recommended)
3. Check CUDA version compatibility with your GPU

### Problem: Memory issues during model loading
**Solutions**:
1. Use GPU with at least 16GB VRAM
2. Enable model CPU offloading in the code
3. Use smaller batch sizes
4. Consider using `torch.float16` precision

## RunPod Deployment Issues

### Problem: Container fails to start
**Solutions**:
1. Check container logs in RunPod dashboard
2. Ensure correct port mapping (8000)
3. Verify environment variables are set correctly
4. Check if model files are downloading properly

### Problem: Model loading timeout
**Solutions**:
1. Increase container startup timeout
2. Pre-download models to volume storage
3. Use faster storage options in RunPod
4. Monitor GPU memory usage

### Problem: API requests failing
**Solutions**:
1. Check if the handler is running: `curl http://localhost:8000/health`
2. Verify input format (base64 images)
3. Check request size limits
4. Monitor container resources

## Model Performance Issues

### Problem: Slow inference times
**Solutions**:
1. Use GPU instead of CPU
2. Enable attention slicing: `pipe.enable_attention_slicing()`
3. Use xformers for memory efficiency
4. Reduce number of inference steps (20-30 is usually sufficient)

### Problem: Poor quality results
**Solutions**:
1. Use higher resolution input images (512x768 recommended)
2. Improve prompts with more descriptive text
3. Adjust guidance scale (7.5 is default)
4. Preprocess images for better quality

## Commercial Licensing Issues

### Problem: Using model commercially without license
**Solutions**:
1. Contact Kwai-Kolors: kwai-kolors@kuaishou.com
2. Fill out commercial licensing questionnaire
3. Wait for approval before commercial deployment
4. Academic use is freely permitted

## Local Development Issues

### Problem: Dependencies not installing locally
**Solutions**:
1. Use Python 3.10 (recommended version)
2. Create virtual environment: `python -m venv venv`
3. Install PyTorch first: `pip install torch torchvision`
4. Install other dependencies: `pip install -r requirements.txt`

### Problem: CUDA not available locally
**Solutions**:
1. Install CUDA toolkit from NVIDIA
2. Verify installation: `nvidia-smi`
3. Use CPU version for testing: modify device selection in code
4. Consider using Google Colab for GPU access

## API Integration Issues

### Problem: Base64 encoding/decoding errors
**Solutions**:
1. Ensure proper base64 format: `data:image/png;base64,<data>`
2. Remove data URL prefix before decoding
3. Use proper image formats (PNG, JPEG)
4. Check image size limits (16MB max)

### Problem: Flask app not starting
**Solutions**:
1. Check port availability (5000)
2. Install Flask dependencies
3. Set proper environment variables
4. Check file permissions

## Getting Help

1. **Check logs** - Always check container/application logs first
2. **GitHub Issues** - Create an issue with detailed error information
3. **RunPod Support** - Contact RunPod for infrastructure issues
4. **Community** - Join AI/ML communities for general help

## Useful Commands

```bash
# Build Docker image
docker build -t kolors-tryon .

# Run locally for testing
docker run -p 8000:8000 kolors-tryon

# Check container logs
docker logs <container_id>

# Test API endpoint
curl -X POST http://localhost:8000/api/try-on \
  -H "Content-Type: application/json" \
  -d '{"person_image": "base64...", "clothing_image": "base64..."}'

# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```
