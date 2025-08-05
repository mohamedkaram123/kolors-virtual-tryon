import runpod
import base64
import io
import time
from PIL import Image
import json

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
    return img_str

def simple_image_blend(person_image, clothing_image):
    """Simple image blending as a placeholder for actual AI model"""
    # Resize images to same size
    person_image = person_image.resize((512, 768))
    clothing_image = clothing_image.resize((512, 768))
    
    # Simple alpha blending
    result = Image.blend(person_image, clothing_image, 0.3)
    return result

def handler(job):
    """RunPod serverless handler function"""
    start_time = time.time()
    
    try:
        # Get job input
        job_input = job.get("input", {})
        
        print(f"Received job input: {list(job_input.keys())}")
        
        # Validate required inputs
        if "person_image" not in job_input or "clothing_image" not in job_input:
            return {
                "error": "Missing required inputs: person_image and clothing_image",
                "status": "error"
            }
        
        # Decode input images
        print("Decoding input images...")
        person_image = decode_base64_image(job_input["person_image"])
        clothing_image = decode_base64_image(job_input["clothing_image"])
        
        print(f"Person image size: {person_image.size}")
        print(f"Clothing image size: {clothing_image.size}")
        
        # Process (simple blend for now)
        print("Processing images...")
        result_image = simple_image_blend(person_image, clothing_image)
        
        # Encode result
        print("Encoding result...")
        result_base64 = encode_image_to_base64(result_image)
        
        processing_time = time.time() - start_time
        
        return {
            "result_image": result_base64,
            "processing_time": round(processing_time, 2),
            "status": "success",
            "message": "Simple image blending completed (placeholder for AI model)"
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

# Health check function
def health_check():
    """Simple health check"""
    return {
        "status": "healthy",
        "message": "Simple handler is running",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    print("Starting simple RunPod handler...")
    print("This is a basic version without AI model - for testing deployment")
    
    # Test the handler locally if needed
    test_mode = False
    
    if test_mode:
        # Simple test
        print("Running in test mode...")
        test_job = {
            "input": {
                "person_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                "clothing_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            }
        }
        result = handler(test_job)
        print(f"Test result: {result}")
    else:
        # Start RunPod serverless
        runpod.serverless.start({"handler": handler})
