# RunPod Deployment Guide

## 🚀 Quick Start (Recommended)

Due to Docker build complexity with the full AI model, we provide multiple deployment approaches:

### Option 1: Simple Test Deployment (Recommended First)

Use this to test your RunPod setup before deploying the full AI model:

1. **Use the minimal Dockerfile**:
   ```bash
   cp Dockerfile.minimal Dockerfile
   ```

2. **Build and test locally**:
   ```bash
   docker build -t kolors-test .
   docker run -p 8000:8000 kolors-test
   ```

3. **Deploy to RunPod**:
   - Push image to your registry
   - Create RunPod serverless endpoint
   - Use the simple handler for testing

### Option 2: Full AI Model Deployment

Once the basic setup works, upgrade to the full model:

1. **Use the main Dockerfile** (with fixed dependencies)
2. **Ensure you have commercial license** from Kwai-Kolors
3. **Use a high-memory GPU** (A100 recommended)

## 📋 Step-by-Step RunPod Deployment

### Step 1: Prepare Your Docker Image

Choose your approach:

**For Testing (Simple)**:
```bash
# Use minimal setup
cp Dockerfile.minimal Dockerfile
cp handler_simple.py handler.py
```

**For Production (Full AI)**:
```bash
# Use full setup (ensure you have Kolors license)
# Keep the main Dockerfile and handler.py
```

### Step 2: Build and Push Docker Image

```bash
# Build the image
docker build -t your-registry/kolors-tryon:latest .

# Push to your registry (Docker Hub, etc.)
docker push your-registry/kolors-tryon:latest
```

### Step 3: Create RunPod Serverless Endpoint

1. **Log into RunPod**: https://runpod.io
2. **Go to Serverless**: Click "Serverless" in the sidebar
3. **Create New Endpoint**: Click "New Endpoint"
4. **Configure**:
   - **Name**: `kolors-virtual-tryon`
   - **Docker Image**: `your-registry/kolors-tryon:latest`
   - **Container Port**: `8000`
   - **Container Disk**: `20GB` (for full model) or `5GB` (for simple)
   - **GPU**: `A100` (for full model) or `RTX 4090` (for simple)

### Step 4: Configure Environment Variables

Add these environment variables in RunPod:
```
PYTHONPATH=/app
TORCH_HOME=/app/models
HF_HOME=/app/models
```

### Step 5: Test Your Deployment

Once deployed, test with:

```bash
curl -X POST https://your-endpoint-url/runsync \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "person_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
      "clothing_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    }
  }'
```

## 🔧 Troubleshooting

### Docker Build Fails
1. **Try the minimal Dockerfile first**: `cp Dockerfile.minimal Dockerfile`
2. **Check internet connection**: Ensure Docker can download packages
3. **Use specific versions**: The updated Dockerfile uses pinned versions
4. **Build with no cache**: `docker build --no-cache -t kolors-tryon .`

### RunPod Container Won't Start
1. **Check logs** in RunPod dashboard
2. **Verify image was pushed** to registry correctly
3. **Check port configuration** (should be 8000)
4. **Ensure sufficient resources** (GPU memory, disk space)

### Model Loading Issues (Full Version)
1. **Use A100 GPU** for sufficient VRAM
2. **Increase timeout** in RunPod settings
3. **Check Kolors license** is properly configured
4. **Monitor GPU memory** usage

## 📊 Resource Requirements

### Simple Version (Testing)
- **GPU**: RTX 4090 or similar
- **VRAM**: 8GB minimum
- **Disk**: 5GB
- **RAM**: 16GB

### Full AI Version (Production)
- **GPU**: A100 (recommended)
- **VRAM**: 24GB minimum
- **Disk**: 20GB
- **RAM**: 32GB

## 🔐 Commercial Licensing

Before using the full AI model commercially:

1. **Contact Kwai-Kolors**: kwai-kolors@kuaishou.com
2. **Request licensing questionnaire**
3. **Wait for approval**
4. **Academic use is free**

## 📞 Support

- **GitHub Issues**: For code-related problems
- **RunPod Support**: For infrastructure issues
- **Kolors Team**: For licensing questions

## 🎯 Next Steps

1. **Start with simple deployment** to test setup
2. **Upgrade to full AI model** once basic setup works
3. **Integrate with your application** using the API
4. **Scale as needed** with RunPod's auto-scaling
