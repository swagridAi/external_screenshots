"""
Main application for Screenshot to Table converter.
"""
import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory

# Import configuration
from config import DEBUG, HOST, PORT

# Import modules
from modules.screenshot import capture_screenshot, get_screenshot_response
from modules.image_processing import save_cropped_image, create_temp_image, cleanup_temp_file
from modules.table_extraction import extract_table_from_image
from modules.utils import convert_to_csv, setup_logger, format_timestamp

# Setup logger
logger = setup_logger()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/request-screenshot')
def request_screenshot():
    """Endpoint to request a screenshot from the sender"""
    logger.info("Screenshot requested")
    
    success, result = capture_screenshot()
    
    if success:
        # result is BytesIO with image data
        return get_screenshot_response(result)
    else:
        # result is error message
        logger.error(f"Screenshot request failed: {result}")
        return jsonify({'success': False, 'error': result}), 500

@app.route('/save-cropped', methods=['POST'])
def save_cropped():
    """Endpoint to save a cropped image"""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
            
        image_data = data['image']
        success, result = save_cropped_image(image_data)
        
        if success:
            # result is filename
            return jsonify({'success': True, 'filename': result})
        else:
            # result is error message
            return jsonify({'success': False, 'error': result}), 500
            
    except Exception as e:
        logger.exception("Error in save_cropped endpoint")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/extract-table', methods=['POST'])
def extract_table():
    """Endpoint to extract table data from an image"""
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
            
        # Create temporary image file
        success, temp_file = create_temp_image(data['image'])
        
        if not success:
            # temp_file is error message
            return jsonify({'success': False, 'error': temp_file}), 500
        
        # Extract table data
        success, result = extract_table_from_image(temp_file)
        
        # Clean up temp file
        cleanup_temp_file(temp_file)
        
        if success:
            # result is table data
            return jsonify({
                'success': True,
                'table_data': result
            })
        else:
            # result is error message
            return jsonify({'success': False, 'error': result}), 500
            
    except Exception as e:
        logger.exception("Error in extract_table endpoint")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download-csv', methods=['POST'])
def download_csv():
    """Endpoint to download table data as CSV"""
    try:
        data = request.json
        if not data or 'table_data' not in data:
            return jsonify({'success': False, 'error': 'No table data provided'}), 400
            
        csv_data = convert_to_csv(data['table_data'])
        timestamp = format_timestamp()
        
        return jsonify({
            'success': True,
            'filename': f'table_data_{timestamp}.csv',
            'data': csv_data
        })
        
    except Exception as e:
        logger.exception("Error in download_csv endpoint")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    logger.info(f"Starting Screenshot to Table application on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)