@echo off
title VisionSpeak Setup
cd /d "%~dp0"
echo Checking Python...
py -3.11 --version
if errorlevel 1 (
  echo Python 3.11 was not found. Install Python 3.11 64-bit and enable Add Python to PATH.
  pause
  exit /b 1
)
if not exist .venv (
  py -3.11 -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo Setup failed. Check your internet connection and Python installation.
  pause
  exit /b 1
)
echo Setup complete. Run run.bat.
pause
