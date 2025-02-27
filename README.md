# Screenshot to Table Converter

This application allows you to:
1. Capture screenshots from a remote machine
2. Crop tables from those screenshots
3. Extract tabular data using AI
4. Export the data as CSV or JSON

## Setup Instructions

### 1. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install flask requests pillow openai python-dotenv
```

### 2. Configure API Keys (Choose one method)

#### Method A: Using secrets.py (Preferred)

```bash
# Copy the template file
cp secrets.py.example secrets.py

# Edit secrets.py and add your OpenAI API key
# OPENAI_API_KEY = "your_openai_api_key_here"
```

#### Method B: Using Environment Variables

```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your configuration
# Particularly:
# - OPENAI_API_KEY (your OpenAI API key)
# - SENDER_IP (the IP address of the machine sending screenshots)
```

### 3. Start the Sender on Remote Machine

On the machine you want to capture screenshots from:

```bash
# Install dependencies
pip install flask pyautogui

# Run the sender script
python sender.py
```

### 4. Start the Receiver (This Application)

```bash
# Start the application
python app.py
```

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5001
```

## Usage

1. Press **spacebar** or click **"Capture Screenshot"** to request a screenshot from the sender
2. **Crop** the table area you want to extract data from
3. Click **"Extract Table Data"** to process the image with AI
4. View the table data and **download** as CSV or JSON as needed

## Security Notes

- API keys and other sensitive information are kept in `secrets.py` or `.env` files
- These files are excluded from Git to prevent accidentally committing API keys
- See `docs/API_KEYS.md` for more details on managing secrets securely

## Project Structure

```
screenshot_to_table/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── secrets.py.example      # Template for API keys (copy to secrets.py)
├── .env.example            # Template for environment variables (copy to .env)
├── modules/
│   ├── screenshot.py       # Screenshot capture functionality
│   ├── image_processing.py # Image manipulation (cropping, saving)
│   ├── table_extraction.py # OpenAI table extraction logic
│   └── utils.py            # Utility functions
├── static/                 # Frontend assets
├── templates/              # HTML templates
└── docs/                   # Documentation
```

## Troubleshooting

- Ensure the sender machine is running the sender script
- Verify the IP address in your configuration is correct
- Check that your OpenAI API key is valid
- Look for error messages in the terminal or web interface