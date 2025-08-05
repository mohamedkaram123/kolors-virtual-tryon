import runpod
import torch
import base64
import io
import time
import os
from PIL import Image
from diffusers import StableDiffusionXLPipeline
import numpy as np
import cv2

# Global variables for model loading
pipe = None
device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    """Load the Kolors model once when container starts"""
    global pipe
    
    print("Loading Kolors Virtual Try-On model...")
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
        
        print(f"Model loaded successfully on {device}")
        return True
        
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

def decode_base64_image(base64_string):
    """Convert base64 string to PIL Image"""
    try:
        # Remove data URL prefix if present
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
    return img_str

def preprocess_images(person_image, clothing_image):
    """Preprocess images for virtual try-on"""
    # Resize images to standard size
    target_size = (512, 768)  # Width x Height
    
    person_image = person_image.resize(target_size, Image.Resampling.LANCZOS)
    clothing_image = clothing_image.resize((512, 512), Image.Resampling.LANCZOS)
    
    return person_image, clothing_image

def process_virtual_tryon(person_image, clothing_image, prompt=""):
    """Process virtual try-on using Kolors model"""
    global pipe
    
    if pipe is None:
        raise RuntimeError("Model not loaded")
    
    try:
        # Preprocess images
        person_image, clothing_image = preprocess_images(person_image, clothing_image)
        
        # Create prompt for virtual try-on
        if not prompt:
            prompt = "photorealistic, high quality, detailed clothing, perfect fit, natural lighting, professional photography"
        
        negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs, missing limbs, floating limbs, disconnected limbs, malformed hands, poorly drawn hands, mutated hands, extra fingers, fewer fingers, bad proportions, mutation, deformed, ugly, disgusting, amputation"
        
        # Generate result using the pipeline
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

def handler(job):
    """RunPod serverless handler function"""
    start_time = time.time()
    
    try:
        # Get job input
        job_input = job.get("input", {})
        
        # Validate required inputs
        if "person_image" not in job_input or "clothing_image" not in job_input:
            return {
                "error": "Missing required inputs: person_image and clothing_image"
            }
        
        # Decode input images
        print("Decoding input images...")
        person_image = decode_base64_image(job_input["person_image"])
        clothing_image = decode_base64_image(job_input["clothing_image"])
        
        # Get optional prompt
        prompt = job_input.get("prompt", "")
        
        # Process virtual try-on
        print("Processing virtual try-on...")
        result_image = process_virtual_tryon(person_image, clothing_image, prompt)
        
        # Encode result
        print("Encoding result...")
        result_base64 = encode_image_to_base64(result_image)
        
        processing_time = time.time() - start_time
        
        return {
            "result_image": result_base64,
            "processing_time": round(processing_time, 2),
            "status": "success"
        }
        
    except Exception as e:
        processing_time = time.time() - start_time
        error_msg = str(e)
        print(f"Error in handler: {error_msg}")
        
        return {
            "error": error_msg,
            "processing_time": round(processing_time, 2),
            "status": "error"
        }

# Initialize model when container starts
if __name__ == "__main__":
    print("Initializing Kolors Virtual Try-On handler...")
    
    # Load model
    model_loaded = load_model()
    
    if model_loaded:
        print("Starting RunPod serverless handler...")
        runpod.serverless.start({"handler": handler})
    else:
        print("Failed to load model. Exiting...")
        exit(1)
