from flask import Flask, request, jsonify, render_template, send_from_directory
import base64
import io
import os
import time
from PIL import Image
import torch
from diffusers import StableDiffusionXLPipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables
pipe = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    """Load the Kolors model"""
    global pipe
    
    logger.info("Loading Kolors Virtual Try-On model...")
    try:
        pipe = StableDiffusionXLPipeline.from_pretrained(
            "Kwai-Kolors/Kolors",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True,
            variant="fp16" if device == "cuda" else None
        )
        
        if device == "cuda":
            pipe = pipe.to("cuda")
            pipe.enable_model_cpu_offload()
            pipe.enable_attention_slicing()
        
        logger.info(f"Model loaded successfully on {device}")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

def decode_base64_image(base64_string):
    """Convert base64 string to PIL Image"""
    try:
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image.convert('RGB')
    except Exception as e:
        raise ValueError(f"Invalid base64 image: {str(e)}")

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def process_virtual_tryon(person_image, clothing_image, prompt=""):
    """Process virtual try-on using Kolors model"""
    global pipe
    
    if pipe is None:
        raise RuntimeError("Model not loaded")
    
    try:
        # Resize images
        target_size = (512, 768)
        person_image = person_image.resize(target_size, Image.Resampling.LANCZOS)
        clothing_image = clothing_image.resize((512, 512), Image.Resampling.LANCZOS)
        
        # Create prompt
        if not prompt:
            prompt = "photorealistic, high quality, detailed clothing, perfect fit, natural lighting, professional photography"
        
        negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, floating limbs, disconnected limbs, malformed hands, poorly drawn hands, mutated hands, extra fingers, fewer fingers, bad proportions, mutation, deformed, ugly, disgusting, amputation"
        
        # Generate result
        with torch.autocast(device):
            result = pipe(
                prompt=prompt,
                image=person_image,
                control_image=clothing_image,
                num_inference_steps=20,
                guidance_scale=7.5,
                strength=0.8,
                generator=torch.Generator(device=device).manual_seed(42)
            )
        
        return result.images[0]
        
    except Exception as e:
        raise RuntimeError(f"Virtual try-on processing failed: {str(e)}")

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/try-on', methods=['POST'])
def api_try_on():
    """API endpoint for virtual try-on"""
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'person_image' not in data or 'clothing_image' not in data:
            return jsonify({
                'error': 'Missing required fields: person_image and clothing_image'
            }), 400
        
        # Decode images
        person_image = decode_base64_image(data['person_image'])
        clothing_image = decode_base64_image(data['clothing_image'])
        
        # Get optional prompt
        prompt = data.get('prompt', '')
        
        # Process virtual try-on
        result_image = process_virtual_tryon(person_image, clothing_image, prompt)
        
        # Encode result
        result_base64 = encode_image_to_base64(result_image)
        
        processing_time = time.time() - start_time
        
        return jsonify({
            'result_image': result_base64,
            'processing_time': round(processing_time, 2),
            'status': 'success'
        })
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error in try-on API: {str(e)}")
        
        return jsonify({
            'error': str(e),
            'processing_time': round(processing_time, 2),
            'status': 'error'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': pipe is not None,
        'device': device
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Load model on startup
    logger.info("Starting Kolors Virtual Try-On Flask App...")
    
    if load_model():
        logger.info("Model loaded successfully. Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        logger.error("Failed to load model. Exiting...")
        exit(1)
