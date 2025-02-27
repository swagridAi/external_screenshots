@echo off
:: Screenshot to Table Installation Script for Windows
setlocal enabledelayedexpansion

:: Set colors for output
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BOLD=[1m"
set "NC=[0m"

:: Header
echo %BOLD%===============================================%NC%
echo %BOLD%  Screenshot to Table Converter - Installation  %NC%
echo %BOLD%===============================================%NC%
echo.

:: Check if Python 3 is installed
python --version > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%%BOLD%[!] Python is not installed or not in PATH.%NC%
    echo     Please install Python 3.8 or newer from python.org
    echo     Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Check Python version (need 3.8+)
for /f "tokens=2" %%a in ('python --version 2^>^&1') do set python_version=%%a
for /f "tokens=1,2 delims=." %%a in ("!python_version!") do (
    set major=%%a
    set minor=%%b
)

if !major! lss 3 (
    echo %RED%%BOLD%[!] Python !python_version! detected. This project requires Python 3.8 or newer.%NC%
    pause
    exit /b 1
)

if !major! equ 3 (
    if !minor! lss 8 (
        echo %RED%%BOLD%[!] Python !python_version! detected. This project requires Python 3.8 or newer.%NC%
        pause
        exit /b 1
    )
)

echo %GREEN%%BOLD%[+] Python !python_version! detected.%NC%

:: Create and activate virtual environment
echo %GREEN%%BOLD%[+] Setting up virtual environment...%NC%

if exist venv (
    echo %YELLOW%%BOLD%[!] Virtual environment already exists. Using existing environment.%NC%
) else (
    python -m venv venv || (
        echo %RED%%BOLD%[!] Failed to create virtual environment.%NC%
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate.bat || (
    echo %RED%%BOLD%[!] Failed to activate virtual environment.%NC%
    pause
    exit /b 1
)

:: Install dependencies
echo %GREEN%%BOLD%[+] Installing dependencies...%NC%
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || (
    echo %RED%%BOLD%[!] Failed to install dependencies.%NC%
    pause
    exit /b 1
)

:: Create configuration files from templates
echo %GREEN%%BOLD%[+] Setting up configuration files...%NC%

:: Create .env if it doesn't exist
if not exist .env (
    copy .env.example .env > nul
    echo %GREEN%    Created .env file from template%NC%
) else (
    echo %YELLOW%    .env file already exists, skipping.%NC%
)

:: Create api_keys.py if it doesn't exist
if not exist api_keys.py (
    copy api_keys.py.example api_keys.py > nul
    echo %GREEN%    Created api_keys.py file from template%NC%
) else (
    echo %YELLOW%    api_keys.py file already exists, skipping.%NC%
)

:: Create necessary directories
echo %GREEN%%BOLD%[+] Creating required folders...%NC%

:: Create data directory structure
if not exist data mkdir data
if not exist data\screenshots mkdir data\screenshots
if not exist data\cropped_screenshots mkdir data\cropped_screenshots
if not exist data\temp mkdir data\temp

:: OpenAI API Key setup
echo %GREEN%%BOLD%[+] Configuration setup...%NC%
echo.
set /p configure_api="%BOLD%Do you want to configure your OpenAI API key now? (y/n):%NC% "

if /i "!configure_api!"=="y" (
    set /p api_key="%BOLD%Enter your OpenAI API key:%NC% "
    
    :: Add to api_keys.py - using PowerShell for reliable file manipulation
    powershell -Command "(Get-Content api_keys.py) -replace 'your_openai_api_key_here', '!api_key!' | Set-Content api_keys.py"
    echo %GREEN%    API key added to api_keys.py%NC%
) else (
    echo %YELLOW%%BOLD%[!] You will need to add your OpenAI API key to api_keys.py before using the table extraction feature.%NC%
)

:: Sender IP configuration
echo.
set /p configure_ip="%BOLD%Do you want to configure the sender IP address now? (y/n):%NC% "

if /i "!configure_ip!"=="y" (
    set /p sender_ip="%BOLD%Enter the IP address of the sender machine:%NC% "
    
    :: Add to .env - using PowerShell for reliable file manipulation
    powershell -Command "(Get-Content .env) -replace 'SENDER_IP=.*', 'SENDER_IP=!sender_ip!' | Set-Content .env"
    echo %GREEN%    Sender IP added to .env%NC%
) else (
    echo %YELLOW%%BOLD%[!] You will need to add the sender IP address to .env before capturing screenshots.%NC%
)

:: Installation complete
echo.
echo %GREEN%%BOLD%[+] Installation complete!%NC%
echo.
echo %BOLD%==================================================%NC%
echo %BOLD%  To start the application:%NC%
echo %BOLD%==================================================%NC%
echo.
echo  1. Activate the virtual environment:
echo     %GREEN%venv\Scripts\activate%NC%
echo.
echo  2. Run the application:
echo     %GREEN%python app.py%NC%
echo.
echo %YELLOW%%BOLD%[!] Make sure the sender script is running on the other machine.%NC%
echo.

pause
exit /b 0