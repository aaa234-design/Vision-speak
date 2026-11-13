# VisionSpeak

VisionSpeak is a Windows-friendly object detection app built with Streamlit, Ultralytics YOLO-World, OpenCV, and offline text-to-speech.

## Features
- Detects a curated set of 100 everyday object categories.
- Image upload and webcam snapshot detection.
- Adjustable confidence and image size.
- English voice announcements with optional Urdu voice selection when a compatible Windows speech voice is installed.
- CPU mode supported; no NVIDIA GPU is required.

## Requirements
- Windows 10/11
- Python 3.11 (64-bit recommended)
- Internet connection on first run to download the YOLO-World model

## Run
1. Download or clone this repository.
2. Double-click `setup.bat`.
3. Double-click `run.bat`.
4. Upload an image or take a webcam snapshot in the browser.

The first detection can take longer while the model is downloaded and initialized. CPU detection is slower than NVIDIA GPU detection. For best CPU performance, use smaller images.

## Voice notes
English offline speech normally uses an installed Windows SAPI voice. Urdu speech is available only if Windows has a compatible Urdu text-to-speech voice installed; otherwise the app reports that no Urdu voice is available.

## Object categories
The model is prompted with 100 everyday categories. Open-vocabulary detection is approximate: visually similar categories may be confused, and not every object is guaranteed to be detected.
