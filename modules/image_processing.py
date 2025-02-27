"""
Module for handling image processing operations like cropping and saving.
"""
import os
import base64
from io import BytesIO
from datetime import datetime
import logging
from PIL import Image

from config import CROPPED_SCREENSHOTS_DIR, TEMP_DIR

logger = logging.getLogger(__name__)

def save_cropped_image(base64_image):
    """
    Saves a base64-encoded image to the cropped screenshots directory
    
    Args:
        base64_image (str): Base64-encoded image data
        
    Returns:
        tuple: (success, filename_or_error)
            - If successful, returns (True, saved filename)
            - If failed, returns (False, error message)
    """
    try:
        # Extract the base64 data (remove data:image/png;base64, prefix)
        if ',' in base64_image:
            base64_data = base64_image.split(',', 1)[1]
        else:
            base64_data = base64_image
            
        # Decode base64 data
        image_bytes = base64.b64decode(base64_data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CROPPED_SCREENSHOTS_DIR}/cropped_{timestamp}.png"
        
        # Save the image
        with open(filename, 'wb') as f:
            f.write(image_bytes)
            
        logger.info(f"Cropped image saved to {filename}")
        
        return True, filename
        
    except Exception as e:
        error_msg = f"Error saving cropped image: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def create_temp_image(base64_image):
    """
    Creates a temporary image file from base64 data for processing
    
    Args:
        base64_image (str): Base64-encoded image data
        
    Returns:
        tuple: (success, filename_or_error)
            - If successful, returns (True, temp filename)
            - If failed, returns (False, error message)
    """
    try:
        # Extract the base64 data
        if ',' in base64_image:
            base64_data = base64_image.split(',', 1)[1]
        else:
            base64_data = base64_image
            
        # Decode base64 data
        image_bytes = base64.b64decode(base64_data)
        
        # Generate temporary filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"{TEMP_DIR}/temp_image_{timestamp}.png"
        
        # Save the image
        with open(temp_filename, 'wb') as f:
            f.write(image_bytes)
            
        logger.info(f"Temporary image created at {temp_filename}")
        
        return True, temp_filename
        
    except Exception as e:
        error_msg = f"Error creating temporary image: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def cleanup_temp_file(filename):
    """
    Removes a temporary file
    
    Args:
        filename (str): Path to the file to remove
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if os.path.exists(filename):
            os.remove(filename)
            logger.info(f"Temporary file {filename} removed")
            return True
        return False
    except Exception as e:
        logger.error(f"Error removing temporary file {filename}: {str(e)}")
        return False

def get_image_dimensions(image_path):
    """
    Gets the dimensions of an image
    
    Args:
        image_path (str): Path to the image
        
    Returns:
        tuple: (width, height) or None if error
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"Error getting image dimensions: {str(e)}")
        return None