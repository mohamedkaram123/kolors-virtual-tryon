#!/bin/bash

# Kolors Virtual Try-On Deployment Script for RunPod
# This script helps build and deploy the Docker container

set -e

echo "🚀 Kolors Virtual Try-On Deployment Script"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Get registry and tag from arguments or use defaults
REGISTRY=${1:-"your-registry"}
TAG=${2:-"latest"}
IMAGE_NAME="$REGISTRY/kolors-virtual-tryon:$TAG"

echo "📦 Building Docker image: $IMAGE_NAME"

# Build the Docker image
docker build -t "$IMAGE_NAME" . --no-cache

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    
    # Ask if user wants to push to registry
    read -p "🔄 Do you want to push to registry? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Pushing to registry..."
        docker push "$IMAGE_NAME"
        
        if [ $? -eq 0 ]; then
            echo "✅ Image pushed successfully!"
            echo "🎯 You can now use this image in RunPod: $IMAGE_NAME"
        else
            echo "❌ Failed to push image to registry"
            exit 1
        fi
    fi
    
    echo ""
    echo "🎉 Deployment preparation complete!"
    echo ""
    echo "📋 Next steps for RunPod deployment:"
    echo "1. Log into your RunPod account"
    echo "2. Create a new serverless endpoint"
    echo "3. Use Docker image: $IMAGE_NAME"
    echo "4. Set container port: 8000"
    echo "5. Configure environment variables if needed"
    echo ""
    echo "🔗 RunPod Template Configuration:"
    echo "   - Container Disk: 20GB"
    echo "   - Volume: 10GB"
    echo "   - GPU: A100 or RTX 4090 recommended"
    echo ""
    
else
    echo "❌ Docker build failed!"
    echo "💡 Try the following troubleshooting steps:"
    echo "1. Check your internet connection"
    echo "2. Ensure Docker has enough disk space"
    echo "3. Review the error messages above"
    echo "4. Try building with --no-cache flag"
    exit 1
fi
