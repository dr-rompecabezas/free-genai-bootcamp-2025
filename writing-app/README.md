# Sitelen Pona Character Recognition App

A Streamlit-based web application for recognizing Sitelen Pona characters through computer vision techniques. The app uses classical computer vision methods like template matching and feature detection instead of machine learning approaches.

## Features

- Multiple ways to input characters:
  - Interactive canvas for drawing directly in the browser
  - Upload images of hand-drawn characters
  - Capture characters using your webcam in real-time
- Real-time character recognition
- Template-based matching system
- Pre-processed template library included
- Simple and intuitive user interface

## Technical Approach

The app uses an image preprocessing pipeline that:

- Centers each character
- Normalizes size to a standard dimension
- Converts images to binary format
- Compares drawn characters with a template library using multiple comparison methods

## Requirements

- Python 3.11 or higher
- Dependencies listed in `pyproject.toml`

## Setup and Running

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   ```

2. Install dependencies using your preferred package manager:

   Using `uv` (recommended):

   ```bash
   uv sync
   ```

   Using `pip` (reading from pyproject.toml):

   ```bash
   pip install .
   ```

   Using `pip-tools` (if the above does not work):

   ```bash
   pip install pip-tools
   pip-compile pyproject.toml  # Generate requirements.txt from pyproject.toml
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

The app will open in your default web browser. You can start drawing characters on the canvas and the app will attempt to recognize them in real-time. A dropdown menu will provide options for the two additional image input methods: file upload and webcam capture.

## Project Structure

- `app.py` - Main application code with Streamlit interface and recognition logic
- `templates/` - Directory containing preprocessed template images
- `sitelen_pona_svgs/` - Original SVG files for reference
- `scripts/` - Utility scripts used for initial setup (**Note:** These scripts are included for reference only and are not meant to be run)

## Notes

The `scripts/` directory contains the original web scraping and image processing scripts used to create the template library. These scripts are provided for reference only and are not needed for running the application. Please refer to `scripts/README.md` for more details about the data collection process and legal considerations.

## License

The template images are derived from content available under CC BY-SA 3.0 license from the Sona Pona Wiki.
