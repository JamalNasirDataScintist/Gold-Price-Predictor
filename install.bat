@echo off
title Gold Predictor Installation - Python 3.10.11
color 0B

echo ========================================
echo    INSTALLATION FOR PYTHON 3.10.11
echo ========================================
echo.

echo Step 1: Checking Python version...
python --version

echo.
echo Step 2: Creating virtual environment...
python -m venv venv

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 4: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 5: Installing packages...
pip install -r requirements.txt

echo.
echo Step 6: Installing PyAudio for voice...
pip install pipwin
pipwin install pyaudio

echo.
echo Step 7: Creating directories...
if not exist "data" mkdir data
if not exist "models" mkdir models
if not exist "voice" mkdir voice

echo.
echo ========================================
echo    ✅ INSTALLATION COMPLETE!
echo ========================================
echo.
echo To run the application:
echo 1. Double-click run.bat
echo 2. Or run: venv\Scripts\activate.bat
echo 3. Then: streamlit run streamlit_app.py
echo.
echo First time setup:
echo - Click "Get Current Price" 5-10 times
echo - Click "Train Model" in sidebar
echo - Now use voice commands!
echo.
pause