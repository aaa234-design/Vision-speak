@echo off
title VisionSpeak
cd /d "%~dp0"
if not exist .venv\Scripts\activate.bat (
  echo Please run setup.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate
python -m streamlit run app.py
pause
