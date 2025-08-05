import runpod
import base64
import time
import json
import io
from PIL import Image, ImageEnhance

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

def process_virtual_tryon(person_image, clothing_image):
    """Process virtual try-on by blending images"""
    try:
        # Resize images to standard size
        target_size = (512, 768)  # Width x Height for person
        clothing_size = (512, 512)  # Square for clothing
        
        # Resize person image
        person_resized = person_image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Resize clothing image
        clothing_resized = clothing_image.resize(clothing_size, Image.Resampling.LANCZOS)
        
        # Create a clothing overlay on the person image
        # Position clothing in the center-upper area of the person
        overlay_position = (0, 128)  # Start 128 pixels from top
        
        # Create a copy of the person image
        result = person_resized.copy()
        
        # Paste clothing with some transparency
        clothing_with_alpha = clothing_resized.copy()
        clothing_with_alpha.putalpha(180)  # Semi-transparent
        
        # Convert result to RGBA for blending
        result = result.convert('RGBA')
        
        # Paste the clothing onto the person
        result.paste(clothing_with_alpha, overlay_position, clothing_with_alpha)
        
        # Convert back to RGB
        result = result.convert('RGB')
        
        # Enhance the result
        enhancer = ImageEnhance.Contrast(result)
        result = enhancer.enhance(1.1)
        
        enhancer = ImageEnhance.Color(result)
        result = enhancer.enhance(1.05)
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"Image processing failed: {str(e)}")

def handler(job):
    """Upgraded RunPod handler with real image processing"""
    start_time = time.time()
    
    try:
        # Get job input
        job_input = job.get("input", {})
        
        print(f"Received job with keys: {list(job_input.keys())}")
        
        # Simple validation
        if "person_image" not in job_input:
            return {
                "error": "Missing person_image input",
                "status": "error"
            }
        
        if "clothing_image" not in job_input:
            return {
                "error": "Missing clothing_image input", 
                "status": "error"
            }
        
        # Decode input images
        print("Decoding input images...")
        person_image = decode_base64_image(job_input["person_image"])
        clothing_image = decode_base64_image(job_input["clothing_image"])
        
        print(f"Person image size: {person_image.size}")
        print(f"Clothing image size: {clothing_image.size}")
        
        # Process virtual try-on
        print("Processing virtual try-on...")
        result_image = process_virtual_tryon(person_image, clothing_image)
        
        print(f"Result image size: {result_image.size}")
        
        # Encode result image
        print("Encoding result image...")
        result_base64 = encode_image_to_base64(result_image)
        
        processing_time = time.time() - start_time
        
        return {
            "result_image": result_base64,
            "processing_time": round(processing_time, 2),
            "status": "success",
            "message": "Virtual try-on completed! Images processed and blended.",
            "input_info": {
                "person_image_size": person_image.size,
                "clothing_image_size": clothing_image.size,
                "result_image_size": result_image.size
            }
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

if __name__ == "__main__":
    print("🚀 Starting upgraded RunPod handler...")
    print("This version processes real images with PIL blending!")
    
    # Start RunPod serverless
    runpod.serverless.start({"handler": handler})