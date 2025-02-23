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

## Attempts

Several approaches were explored to recognize and evaluate hand-drawn Sitelen Pona characters. The main challenge was finding a computer vision technique that could effectively compare simple geometric shapes while being tolerant of natural variations in human drawing. Each attempt revealed different aspects of the problem and helped inform potential future solutions.

### 1. Template Matching (`cv2_matchtemplate.app.py`)

First attempt using OpenCV's `cv2.matchTemplate()`. This approach:

- Used template matching to find the best match between the drawn image and template
- Pre-processed images to standardize size and center content
- Challenges: Too sensitive to exact positioning and scaling, didn't handle stylistic variations well

### 2. Feature Matching (`cv2_orb.app.py`)

Second attempt using ORB (Oriented FAST and Rotated BRIEF) feature detection:

- Detected and matched keypoints between drawn image and template
- Used feature matching to calculate similarity score
- Challenges: Sitelen Pona characters are too simple for reliable feature detection, resulted in inconsistent keypoint matching

### 3. Shape Matching (`cv2_matchshape.app.py`)

Third attempt using `cv2.matchShapes()`:

- Compared contours using Hu Moments
- Implemented preprocessing to isolate and normalize shapes
- Added debug visualizations for contours and centroids
- Challenges: Similarity scores didn't align with human perception, adjusting scoring ranges didn't solve fundamental matching issues

Each approach revealed different limitations in computer vision techniques when applied to simple, geometric shapes like Sitelen Pona characters. A new approach might need to consider:

- Custom shape descriptors tailored to Sitelen Pona's geometric nature
- Multiple comparison metrics combined
- Machine learning-based approach trained on variations of each character
