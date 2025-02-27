"""
Module for handling screenshot capture functionality.
"""
import os
import requests
from io import BytesIO
from datetime import datetime
import logging
from flask import send_file

from config import SENDER_URL, SCREENSHOTS_DIR

logger = logging.getLogger(__name__)

def capture_screenshot():
    """
    Requests a screenshot from the sender machine
    
    Returns:
        tuple: (success, response_or_error)
            - If successful, returns (True, BytesIO object with image)
            - If failed, returns (False, error message)
    """
    try:
        # Request screenshot from sender
        capture_url = f"{SENDER_URL}/capture"
        logger.info(f"Requesting screenshot from {capture_url}")
        
        response = requests.get(capture_url, timeout=10)
        
        if response.status_code == 200:
            # Save a copy of the screenshot locally (optional)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{SCREENSHOTS_DIR}/screenshot_{timestamp}.png"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Screenshot saved to {filename}")
            
            # Return the image as BytesIO for immediate use
            return True, BytesIO(response.content)
        else:
            error_msg = f"Failed to capture screenshot. Status code: {response.status_code}"
            logger.error(error_msg)
            return False, error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to sender: {str(e)}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error during screenshot capture: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def get_screenshot_response(image_data):
    """
    Creates a Flask response with the screenshot image
    
    Args:
        image_data (BytesIO): Image data
        
    Returns:
        Response: Flask response object with the image
    """
    return send_file(image_data, mimetype='image/png')