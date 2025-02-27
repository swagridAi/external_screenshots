"""
Module for extracting table data from images using OpenAI's Vision API.
"""
import os
import base64
import json
import logging
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_table_from_image(image_path):
    """
    Extracts table data from an image using OpenAI's Vision API
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        tuple: (success, table_data_or_error)
            - If successful, returns (True, table data dict)
            - If failed, returns (False, error message)
    """
    try:
        # Validate inputs
        if not OPENAI_API_KEY:
            return False, "OpenAI API key is not configured. Please set OPENAI_API_KEY in config."
            
        if not os.path.exists(image_path):
            return False, f"Image file not found: {image_path}"
        
        # Read image file
        with open(image_path, "rb") as image_file:
            # Get base64 encoded image
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Create the prompt
        prompt = [
            {"role": "system", "content": (
                "You are a data extraction assistant specialized in extracting tabular data from images. "
                "Extract all data into a structured format with columns and rows."
            )},
            {"role": "user", "content": [
                {"type": "text", "text": (
                    "Extract the table data from this image. Identify the column headers first, "
                    "then extract each row of data. Return the data as a JSON object with a 'columns' array "
                    "listing all column names, and a 'rows' array of objects where each object has keys "
                    "matching the column names and values from the table cells."
                )},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ]
        
        logger.info("Sending request to OpenAI API for table extraction")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=prompt,
            max_tokens=OPENAI_MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        
        # Parse the response as JSON
        content = response.choices[0].message.content
        table_data = json.loads(content)
        
        logger.info("Received table data from OpenAI API")
        
        # Validate and normalize the response structure
        validated_data = _validate_and_normalize_table_data(table_data)
        
        return True, validated_data
        
    except json.JSONDecodeError as e:
        error_msg = f"Error parsing JSON response from OpenAI: {str(e)}\nResponse content: {content}"
        logger.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"Error extracting table from image: {str(e)}"
        logger.error(error_msg)
        return False, error_msg

def _validate_and_normalize_table_data(table_data):
    """
    Validates and normalizes table data structure
    
    Args:
        table_data (dict): Table data from OpenAI API
        
    Returns:
        dict: Normalized table data with 'columns' and 'rows'
        
    Raises:
        ValueError: If the data structure is invalid and can't be normalized
    """
    # Check if we have a valid structure already
    if 'columns' in table_data and 'rows' in table_data:
        # Validate that rows follow the column structure
        _validate_rows_match_columns(table_data)
        return table_data
        
    # Try to normalize different response formats
    
    # Case 1: List of dictionaries (each dict is a row)
    if isinstance(table_data, list) and len(table_data) > 0 and isinstance(table_data[0], dict):
        columns = list(table_data[0].keys())
        rows = table_data
        return {'columns': columns, 'rows': rows}
        
    # Case 2: Data in a 'data' field
    if 'data' in table_data:
        if isinstance(table_data['data'], list):
            if len(table_data['data']) > 0 and isinstance(table_data['data'][0], dict):
                columns = list(table_data['data'][0].keys())
                rows = table_data['data']
                return {'columns': columns, 'rows': rows}
                
    # Case 3: Headers and rows in separate fields
    if 'headers' in table_data and 'data' in table_data:
        columns = table_data['headers']
        # If data is a 2D array, convert to dictionaries
        if isinstance(table_data['data'], list) and all(isinstance(row, list) for row in table_data['data']):
            rows = [dict(zip(columns, row)) for row in table_data['data']]
            return {'columns': columns, 'rows': rows}
            
    # Failed to normalize
    raise ValueError(
        "Invalid table data structure. Expected 'columns' and 'rows' fields or a normalizable format."
    )

def _validate_rows_match_columns(table_data):
    """
    Validates that all rows have the expected columns
    
    Args:
        table_data (dict): Table data with 'columns' and 'rows'
        
    Returns:
        dict: The original table_data, possibly with missing values filled with None
    """
    columns = table_data['columns']
    
    # Ensure all rows have all columns
    for row in table_data['rows']:
        for column in columns:
            if column not in row:
                row[column] = None
                
    return table_data