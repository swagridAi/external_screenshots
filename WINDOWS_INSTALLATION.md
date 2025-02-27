# Windows Installation Guide

This guide provides step-by-step instructions for installing and setting up the Screenshot to Table application on Windows computers.

## Quick Installation (Automated)

1. **Download the Project Files**
   - Extract the ZIP archive to a location on your computer

2. **Run the Installation Script**
   - Double-click on `install.bat` in the project folder
   - Follow the on-screen prompts to complete the installation
   - The script will set up everything automatically

3. **Start the Application**
   - After installation, activate the virtual environment:
     ```
     venv\Scripts\activate
     ```
   - Run the application:
     ```
     python app.py
     ```

## Manual Installation

If you prefer to install manually, follow these steps:

1. **Prerequisites**
   - Install Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Set Up Virtual Environment**
   - Open Command Prompt in the project folder
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   - With the virtual environment active, run:
     ```
     pip install -r requirements.txt
     ```

4. **Configure API Keys and Settings**
   - Copy the template files:
     ```
     copy secrets.py.example secrets.py
     copy .env.example .env
     ```
   - Edit `secrets.py` and add your OpenAI API key
   - Edit `.env` and add the sender computer's IP address

5. **Create Required Folders**
   - Create these folders if they don't exist:
     ```
     mkdir data\screenshots data\cropped_screenshots data\temp
     ```

## Setting Up the Sender Computer

On the computer you want to capture screenshots from:

1. **Install Python and Dependencies**
   - Install Python 3.8 or newer
   - Install required packages:
     ```
     pip install flask pyautogui
     ```

2. **Run the Sender Script**
   - Copy `sender.py` to this computer
   - Run it with:
     ```
     python sender.py
     ```
   - Note the IP address displayed in the console

3. **Configure Receiver**
   - Use the IP address from step 2 in your `.env` file on the receiver computer

## Folder Structure

The application uses this folder structure:

```
screenshot_to_table\
│
├── app.py                 # Main application
├── config.py              # Configuration settings
├── secrets.py             # API keys (you create this)
├── .env                   # Environment settings (you create this)
│
├── modules\               # Application code
├── static\                # Web assets (CSS, JavaScript)
├── templates\             # HTML templates
│
└── data\                  # Data folders
    ├── screenshots\       # Full screenshots
    ├── cropped_screenshots\ # Cropped images
    └── temp\              # Temporary files
```

## Troubleshooting

- **Python Not Found**: Make sure Python is in your PATH
- **Installation Errors**: Try running Command Prompt as Administrator
- **Connection Issues**: Check that both computers are on the same network
- **Table Extraction Not Working**: Verify your OpenAI API key is correct

## Next Steps

Once installed, refer to the main README.md file for usage instructions.