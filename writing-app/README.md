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
   pip install -e .
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
- `models/` - Pre-converted TFLite model (obtained via `download_model.py`)

## Notes

The `scripts/` directory contains the original web scraping and image processing scripts used to create the template library. These scripts are provided for reference only and are not needed for running the application. Please refer to `scripts/README.md` for more details about the data collection process and legal considerations.

## License

The template images are derived from content available under CC BY-SA 3.0 license from the Sona Pona Wiki.

## Unsuccessful Attempts Using OpenCV

Several approaches were explored to recognize and evaluate hand-drawn Sitelen Pona characters. The main challenge was finding a computer vision technique that could effectively compare simple geometric shapes while being tolerant of natural variations in human drawing. Each attempt revealed different aspects of the problem and helped inform potential future solutions.

   The fundamental issue is that we're trying to do character recognition, but we're treating it as either image matching (OpenCV) or general image classification (EfficientNet). What we really need is a model specifically trained for handwritten character recognition.

### 1. Template Matching (`cv2_matchtemplate.app.py`)

First attempt using OpenCV's `cv2.matchTemplate()`. This approach:

- Used template matching to find the best match between the drawn image and template
- Pre-processed images to standardize size and center content
- Challenges: Too sensitive to exact positioning and scaling, didn't handle stylistic variations well

To run this attempt, execute:

```bash
python cv2_matchtemplate.app.py
```

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

To run this attempt, execute:

```bash
python cv2_matchshape.app.py
```

### 4. MediaPipe with EfficientNet (`mediapipe.app.py`)

This approach used MediaPipe's Vision Tasks API with a pre-trained EfficientNet Lite model to generate embeddings for character recognition. The implementation:

1. Uses MediaPipe's Image Embedder to convert images into feature vectors
2. Compares drawn characters against a template library using cosine similarity
3. Provides similarity scores for all potential matches

To use this version:

1. Download the pre-converted TFLite model:

   ```bash
   python download_model.py
   ```

   This will download the EfficientNet Lite model (approximately 18MB) required for character recognition. The model will be saved in the models directory.

2. Run the app as normal with:

   ```bash
   streamlit run mediapipe.app.py
   ```

#### Results and Limitations

While this approach offered some advantages:

- Easy integration with MediaPipe's vision pipeline
- Pre-trained model for feature extraction
- Fast inference times

It ultimately faced similar challenges to previous attempts:

- The general-purpose image embeddings weren't specific enough to Sitelen Pona's geometric nature
- Struggled to distinguish between similar shapes
- Embeddings were sensitive to variations in drawing style

This experiment reinforced that we need an approach specifically tailored to handwritten character recognition, rather than general image classification or matching.

## Conclusions and Future Directions

Each approach revealed different limitations in computer vision techniques when applied to simple, geometric shapes like Sitelen Pona characters. Our experiments suggest that successful character recognition for Sitelen Pona will likely require:

1. A specialized approach for handwritten character recognition, rather than general image matching or classification
2. Training data that captures the natural variations in how people draw these characters
3. Features that specifically capture the geometric and structural properties of Sitelen Pona

Potential future approaches could include:

- Training a custom CNN on a dataset of hand-drawn Sitelen Pona characters
- Using a pre-trained handwriting recognition model fine-tuned for Sitelen Pona
- Developing custom shape descriptors that better capture the essential features of each character
