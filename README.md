# Kolors Virtual Try-On Deployment

A production-ready deployment of Kolors Virtual Try-On model for RunPod Serverless with GitHub integration.

## 🚀 Features

- **Virtual Try-On**: High-quality clothing try-on using Kolors diffusion model
- **RunPod Serverless**: Scalable GPU deployment
- **REST API**: Easy integration with web applications
- **Docker Ready**: Containerized for consistent deployment
- **Commercial Ready**: Includes licensing compliance

## 📋 Prerequisites

### Commercial License
Before using this commercially, you **must** register with Kwai-Kolors:
1. Email: `kwai-kolors@kuaishou.com`
2. Request commercial licensing questionnaire
3. Wait for approval

### Technical Requirements
- RunPod account
- Docker installed
- Python 3.10+
- CUDA-compatible GPU (for local testing)

## 🛠️ Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/kolors-virtual-tryon.git
cd kolors-virtual-tryon
```

### 2. Local Development
```bash
pip install -r requirements.txt
python app.py
```

### 3. RunPod Deployment
```bash
# Build and push Docker image
docker build -t your-registry/kolors-tryon .
docker push your-registry/kolors-tryon

# Deploy on RunPod using the provided template
```

## 📁 Project Structure

```
kolors-virtual-tryon/
├── app.py              # Main Flask application
├── handler.py          # RunPod serverless handler
├── Dockerfile          # Container configuration
├── requirements.txt    # Python dependencies
├── templates/          # Web interface templates
├── static/            # CSS, JS, images
├── utils/             # Helper functions
└── tests/             # Unit tests
```

## 🔧 API Endpoints

### POST /try-on
Virtual try-on endpoint

**Request:**
```json
{
  "person_image": "base64_encoded_image",
  "clothing_image": "base64_encoded_image",
  "prompt": "optional text prompt"
}
```

**Response:**
```json
{
  "result_image": "base64_encoded_result",
  "processing_time": 2.5
}
```

## 🌐 Web Interface

Access the web interface at `http://localhost:5000` for easy testing and demonstration.

## 📄 License

- **Code**: Apache-2.0 License
- **Model**: Requires commercial registration with Kwai-Kolors
- See [LICENSE](LICENSE) for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For technical issues, create an issue on GitHub.
For commercial licensing, contact: kwai-kolors@kuaishou.com
