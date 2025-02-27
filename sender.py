"""
Screenshot Sender Script

This script runs on the computer you want to capture screenshots from.
It creates a simple web server that responds to screenshot requests.
"""
import os
import sys
import time
import threading
import logging
from datetime import datetime
from flask import Flask, send_file, jsonify

# Try to import pyautogui for screenshot capture
try:
    import pyautogui
except ImportError:
    print("Error: pyautogui module not found.")
    print("Please install it with: pip install pyautogui")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sender.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000
SCREENSHOT_DIR = 'sent_screenshots'

# Create screenshot directory if it doesn't exist
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

@app.route('/')
def home():
    """Home page with status information"""
    return """
    <html>
    <head>
        <title>Screenshot Sender</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #4285F4; }
            .status { padding: 15px; background-color: #d9edf7; border-radius: 4px; margin: 20px 0; }
            .info { margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>Screenshot Sender</h1>
        <div class="status">
            <h2>Status: Running</h2>
            <div class="info">The server is running and ready to capture screenshots.</div>
            <div class="info">IP Address: """ + get_ip_address() + """</div>
            <div class="info">Port: """ + str(PORT) + """</div>
        </div>
        <h3>API Endpoints:</h3>
        <ul>
            <li><strong>/capture</strong> - Capture and return a screenshot</li>
            <li><strong>/status</strong> - Check server status</li>
        </ul>
    </body>
    </html>
    """

@app.route('/capture', methods=['GET'])
def capture():
    """Capture a screenshot and return it"""
    try:
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOT_DIR}/screenshot_{timestamp}.png"
        
        # Take screenshot and save
        logger.info(f"Capturing screenshot to {filename}")
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        
        # Return the screenshot file
        return send_file(filename, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Error capturing screenshot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Return server status"""
    return jsonify({
        'status': 'running',
        'ip_address': get_ip_address(),
        'port': PORT,
        'screenshots_captured': len(os.listdir(SCREENSHOT_DIR))
    })

def get_ip_address():
    """Get the local IP address of this machine"""
    import socket
    try:
        # Create a socket connection to an external server
        # This is a reliable way to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        # Fallback if unable to determine IP
        return "127.0.0.1"

def run_server():
    """Run the Flask server"""
    app.run(host=HOST, port=PORT)

def print_startup_message():
    """Print a startup message with the IP address"""
    ip_address = get_ip_address()
    print("\n" + "=" * 60)
    print(f"  Screenshot Sender Running at http://{ip_address}:{PORT}")
    print("=" * 60)
    print("\nThis computer is now ready to send screenshots on request.")
    print("Important: Make sure this IP address is configured in the receiver app.")
    print("\nPress Ctrl+C to stop the server.\n")

if __name__ == '__main__':
    try:
        # Run Flask in a thread to avoid blocking
        threading.Thread(target=run_server, daemon=True).start()
        
        # Print startup information
        print_startup_message()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down Screenshot Sender...")
        sys.exit(0)