import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import torch
import torchvision.transforms as transforms

def preprocess_person_image(image):
    """Preprocess person image for better virtual try-on results"""
    # Convert PIL to OpenCV format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Apply noise reduction
    denoised = cv2.fastNlMeansDenoisingColored(opencv_image, None, 10, 10, 7, 21)
    
    # Enhance contrast and brightness
    pil_image = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
    
    # Enhance image quality
    enhancer = ImageEnhance.Contrast(pil_image)
    pil_image = enhancer.enhance(1.2)
    
    enhancer = ImageEnhance.Sharpness(pil_image)
    pil_image = enhancer.enhance(1.1)
    
    return pil_image

def preprocess_clothing_image(image):
    """Preprocess clothing image for better virtual try-on results"""
    # Remove background if needed (simple approach)
    # Convert to RGBA
    image = image.convert("RGBA")
    
    # Enhance the clothing image
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.3)
    
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)
    
    return image.convert("RGB")

def create_mask(image, threshold=240):
    """Create a simple mask for clothing segmentation"""
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Create mask where background is white
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Clean up the mask
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return Image.fromarray(mask)

def resize_with_aspect_ratio(image, target_size):
    """Resize image while maintaining aspect ratio"""
    width, height = image.size
    target_width, target_height = target_size
    
    # Calculate aspect ratios
    aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height
    
    if aspect_ratio > target_aspect_ratio:
        # Image is wider than target
        new_width = target_width
        new_height = int(target_width / aspect_ratio)
    else:
        # Image is taller than target
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    
    # Resize image
    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create new image with target size and paste resized image
    result = Image.new('RGB', target_size, (255, 255, 255))
    paste_x = (target_width - new_width) // 2
    paste_y = (target_height - new_height) // 2
    result.paste(resized, (paste_x, paste_y))
    
    return result

def enhance_result_image(image):
    """Post-process the generated result for better quality"""
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.1)
    
    # Enhance color saturation
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.05)
    
    # Slight sharpening
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.05)
    
    return image

def validate_image(image, min_size=(256, 256), max_size=(2048, 2048)):
    """Validate image dimensions and format"""
    width, height = image.size
    
    if width < min_size[0] or height < min_size[1]:
        raise ValueError(f"Image too small. Minimum size: {min_size}")
    
    if width > max_size[0] or height > max_size[1]:
        raise ValueError(f"Image too large. Maximum size: {max_size}")
    
    if image.mode not in ['RGB', 'RGBA']:
        raise ValueError("Image must be in RGB or RGBA format")
    
    return True
