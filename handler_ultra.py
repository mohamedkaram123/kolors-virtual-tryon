import runpod
import base64
import time
import json

def handler(job):
    """Ultra-minimal RunPod handler for testing deployment"""
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
        
        # Get image data lengths (just for testing)
        person_len = len(job_input.get("person_image", ""))
        clothing_len = len(job_input.get("clothing_image", ""))
        
        print(f"Person image data length: {person_len}")
        print(f"Clothing image data length: {clothing_len}")
        
        # Mock processing time
        time.sleep(1)
        
        # Return mock result (base64 encoded 1x1 pixel PNG)
        mock_result = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        
        processing_time = time.time() - start_time
        
        return {
            "result_image": mock_result,
            "processing_time": round(processing_time, 2),
            "status": "success",
            "message": "Ultra-minimal handler working! Ready for full implementation.",
            "input_sizes": {
                "person_image_length": person_len,
                "clothing_image_length": clothing_len
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
    print("🚀 Starting ultra-minimal RunPod handler...")
    print("This version uses only built-in Python libraries + runpod")
    print("Perfect for testing your RunPod deployment pipeline!")
    
    # Start RunPod serverless
    runpod.serverless.start({"handler": handler})
