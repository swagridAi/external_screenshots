"""
Configuration settings for the Screenshot to Table application.
This file combines environment variables and secrets.py (for sensitive data).
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Setup logger for configuration issues
logger = logging.getLogger(__name__)

# Flask Configuration
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5001))

# Screenshot Server Configuration
SENDER_IP = os.getenv('SENDER_IP', '192.168.1.100')  # Replace with actual sender IP
SENDER_PORT = int(os.getenv('SENDER_PORT', 5000))
SENDER_URL = f"http://{SENDER_IP}:{SENDER_PORT}"

# Try to load API keys from secrets.py first (preferred method)
try:
    from secrets import OPENAI_API_KEY as SECRET_OPENAI_API_KEY
    OPENAI_API_KEY = SECRET_OPENAI_API_KEY
    logger.info("Loaded OpenAI API key from secrets.py")
except ImportError:
    # Fall back to environment variables if secrets.py not found
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    if OPENAI_API_KEY:
        logger.info("Loaded OpenAI API key from environment variables")
    else:
        logger.warning(
            "No OpenAI API key found. Please add your API key to secrets.py "
            "or set the OPENAI_API_KEY environment variable."
        )

# Other OpenAI Configuration
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-vision-preview')
OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', 4000))

# File Storage Configuration
SCREENSHOTS_DIR = os.getenv('SCREENSHOTS_DIR', 'data/screenshots')
CROPPED_SCREENSHOTS_DIR = os.getenv('CROPPED_SCREENSHOTS_DIR', 'data/cropped_screenshots')
TEMP_DIR = os.getenv('TEMP_DIR', 'data/temp')

# Ensure directories exist
for directory in [SCREENSHOTS_DIR, CROPPED_SCREENSHOTS_DIR, TEMP_DIR]:
    os.makedirs(directory, exist_ok=True)

# Validate required configuration
def validate_config():
    """Validate that all required configuration is present"""
    if not OPENAI_API_KEY:
        logger.error(
            "OpenAI API key is missing. Table extraction functionality will not work. "
            "Please set up your API key in secrets.py or as an environment variable."
        )
        return False
        
    if SENDER_IP == '192.168.1.100':  # Default value
        logger.warning(
            "Using default sender IP address. Update SENDER_IP in .env or environment variables "
            "with the actual IP address of the sender machine."
        )
        
    return True

# Run validation
CONFIG_VALID = validate_config()