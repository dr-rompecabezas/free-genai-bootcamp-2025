# Sitelen Pona Character Recognition App

[![Writing App Tests](https://github.com/dr-rompecabezas/free-genai-bootcamp-2025/actions/workflows/writing-app-tests.yml/badge.svg)](https://github.com/dr-rompecabezas/free-genai-bootcamp-2025/actions/workflows/writing-app-tests.yml)

A Streamlit-based web application for recognizing hand-drawn Sitelen Pona characters using computer vision and deep learning. The app leverages MediaPipe's Image Embedder with a MobileNetV3-Small backbone to generate robust visual embeddings, enabling accurate recognition of characters despite variations in drawing style.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Table of Contents

- [Features](#features)
- [Technical Approach](#technical-approach)
- [Requirements](#requirements)
- [Setup and Running](#setup-and-running)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [License](#license)
- [Successful Approach Using MediaPipe with MobileNetV3-Small](#successful-approach-using-mediapipe-with-mobilenetv3-small)
  - [Key Components](#key-components)
  - [Advantages](#advantages)
  - [Implementation Details](#implementation-details)
  - [Resources and Documentation](#resources-and-documentation)
- [Unsuccessful Attempts Using OpenCV and MediaPipe with EfficientNet](#unsuccessful-attempts-using-opencv-and-mediapipe-with-efficientnet)
  - [1. Template Matching (`cv2_matchtemplate.app.py`)](#1-template-matching-cv2_matchtemplateapppy)
  - [2. Feature Matching (`cv2_orb.app.py`)](#2-feature-matching-cv2_orbapppy)
  - [3. Shape Matching (`cv2_matchshape.app.py`)](#3-shape-matching-cv2_matchshapeapppy)
  - [4. MediaPipe with EfficientNet (`mediapipe.app.py`)](#4-mediapipe-with-efficientnet-mediapipeapppy)
    - [Results and Limitations](#results-and-limitations)
- [Conclusions and Future Directions](#conclusions-and-future-directions)
- [Screenshots](#screenshots)
  - [Acceptable Solution Using MediaPipe with MobileNet](#acceptable-solution-using-mediapipe-with-mobilenet)
  - [Unacceptable Solutions Using OpenCV and MediaPipe with EfficientNet](#unacceptable-solutions-using-opencv-and-mediapipe-with-efficientnet)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Features

- Multiple ways to input characters:
  - Interactive canvas for drawing directly in the browser
  - Upload images of hand-drawn characters
  - Capture characters using your webcam in real-time
- Real-time character recognition
- Template-based matching system
- Pre-processed template library included
- Simple and intuitive user interface
- Debug mode for visualizing intermediate steps and embeddings
- Comprehensive test suite for UI components and interactions

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

3. Download the pre-converted TFLite model:

   ```bash
   cd scripts
   python download_mobilenet.py
   ```

4. Run the Streamlit app:

   ```bash
   cd ..  # Back to the root directory
   streamlit run app.py
   ```

The app will open in your default web browser. You can start drawing characters on the canvas and the app will attempt to recognize them in real-time. A dropdown menu will provide options for the two additional image input methods: file upload and webcam capture.

## Testing

The app includes a comprehensive test suite using pytest and Streamlit's testing API. The tests cover:

- Basic app functionality (loading, title, tabs)
- UI component interactions (buttons, sliders, toggles)
- State management (session state, callbacks)
- Mode switching and conditional UI elements
- Debug features

To run the tests locally:

1. Activate your virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Install test dependencies:

   ```bash
   pip install pytest
   ```

3. Run the tests:

   ```bash
   python -m pytest tests/test_app.py -v
   ```

The tests are also automatically run via GitHub Actions whenever changes are made to the `writing-app` directory.

## Project Structure

writing-app/
├── app.py              # Main application using MobileNet approach
├── experiments/        # Previous experimental approaches
│   ├── cv2_matchshape.app.py    # Shape matching attempt
│   ├── cv2_matchtemplate.app.py # Template matching attempt
│   ├── cv2_orb.app.py          # Feature matching attempt
│   └── mediapipe.app.py        # MediaPipe with EfficientNet attempt
├── models/            # Model directory
├── scripts/          # Utility scripts
├── sitelen_pona_svgs/ # Original SVG files
├── sitelen_pona_svgs_dark/ # White SVG files for dark mode
├── templates/        # Template images
└── requirements.txt  # Python dependencies

## Notes

The `scripts/` directory contains the original web scraping and image processing scripts used to create the template library. These scripts are provided for reference only and are not needed for running the application. Please refer to `scripts/README.md` for more details about the data collection process and legal considerations.

## License

The template images are derived from content available under CC BY-SA 3.0 license from the Sona Pona Wiki.

## Successful Approach Using MediaPipe with MobileNetV3-Small

After exploring several approaches, we found success using MediaPipe's Image Embedder task with a MobileNetV3-Small backbone. This approach offers several advantages:

### Key Components

1. **Image Preprocessing**:

   - Proper handling of RGBA canvas input with alpha channel masking
   - Consistent 224x224 image size with aspect ratio preservation
   - Center-aligned images on white background
   - Normalized pixel values for model input

2. **Feature Extraction**:

   - MobileNetV3-Small as the backbone architecture
   - MediaPipe's Image Embedder for generating embeddings
   - L2 normalization of embeddings for consistent comparison

3. **Similarity Comparison**:

   - Cosine similarity between normalized embeddings
   - Threshold-based recognition for accepting/rejecting matches

### Advantages

1. **Robust Recognition**:

   - Works well with variations in drawing style
   - Handles different stroke widths and minor distortions
   - Position-invariant within the drawing area

2. **Efficient Processing**:

   - MobileNetV3 is optimized for mobile/web deployment
   - Fast inference times suitable for interactive use
   - Small model size (~9MB)

3. **Easy Integration**:

   - MediaPipe provides a clean Python API
   - Built-in image processing and model management
   - Cross-platform compatibility

### Implementation Details

The system uses a streamlined pipeline:

1. Capture user input (drawing, upload, or webcam)
2. Preprocess the image maintaining aspect ratio
3. Generate embeddings using MediaPipe
4. Compare with template embeddings using cosine similarity
5. Provide immediate feedback with similarity scores

The UI is built with Streamlit and includes:

- Interactive drawing canvas
- Template character display
- Real-time recognition feedback
- Debugging visualizations for understanding the matching process

### Resources and Documentation

For more information about the MediaPipe Image Embedder:

- [MediaPipe Studio Demo](https://mediapipe-studio.webapps.google.com/studio/demo/image_embedder) - Interactive demo of the Image Embedder
- [MediaPipe Image Embedder Documentation](https://ai.google.dev/edge/mediapipe/solutions/vision/image_embedder#configurations_options) - Detailed API documentation and configuration options
- [MobileNetV3-Small Model Details](https://ai.google.dev/edge/mediapipe/solutions/vision/image_embedder#mobilenetv3_model) - Technical specifications and performance characteristics of the MobileNetV3-Small model used for embedding generation

## Unsuccessful Attempts Using OpenCV and MediaPipe with EfficientNet

Several approaches were explored to recognize and evaluate hand-drawn Sitelen Pona characters. The main challenge was finding a computer vision technique that could effectively compare simple geometric shapes while being tolerant of natural variations in human drawing. Each attempt revealed different aspects of the problem and helped inform potential future solutions.

The fundamental issue is that we were trying to do character recognition, but we were treating it as either image matching (OpenCV) or general image classification (EfficientNet). What we really needed is a model specifically trained for handwritten character recognition. In the apparent absence of such a model, we went with MobileNetV3-Small as described above.

To run any of the experimental approaches, execute:

```bash
cd experiments
streamlit run <experiment_file>.app.py
```

See more details below about the experiments.

### 1. Template Matching (`cv2_matchtemplate.app.py`)

First attempt using OpenCV's `cv2.matchTemplate()`. This approach:

- Used template matching to find the best match between the drawn image and template
- Pre-processed images to standardize size and center content
- Challenges: Too sensitive to exact positioning and scaling, didn't handle stylistic variations well

To run this attempt, execute:

```bash
cd experiments
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
cd experiments
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
   cd scripts
   python download_efficientnet.py
   ```

   This will download the EfficientNet Lite model (approximately 18MB) required for character recognition. The model will be saved in the models directory.

2. Run the app as normal with:

   ```bash
   cd ../experiments  # Back to the experiments directory
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

## Screenshots

### Acceptable Solution Using MediaPipe with MobileNet

 -- add screenshots here in GitHub --

### Unacceptable Solutions Using OpenCV and MediaPipe with EfficientNet

Image depicting the debugging of the feature-matching attempt with the OpenCV ORB strategy using sliders to tweak the model's parameters:

![kala-failed-recognition](https://github.com/user-attachments/assets/5e4b06d4-7084-4e6e-ad53-21b4f1744b07)

Image showing the contours (red lines) on the canvas frame and template borders rather than surrounding the glyph itself:

![debug-open-cv-contours](https://github.com/user-attachments/assets/db097fa4-c870-4b3d-b812-503b72a1e6b1)

Image showing the contours correctly wrapping the glyphs and excluding the blank area as well as the data being processed by the model:

![debug-low-accuracy-score](https://github.com/user-attachments/assets/8fa37fd5-e5ed-4ad6-9cc7-1e250a88030b)

Image depicting an obstinately low similarity score despite the obvious similarity of the two shapes:

![cv2.matchShapes_analysis_similarity_score_14](https://github.com/user-attachments/assets/da35f72e-d7b9-49e3-9298-52debb98fa79)

Image from the final set of experiments using OpenCV for pre-processing and MediaPipe for the comparison:

![tawa-char-mismatch](https://github.com/user-attachments/assets/7f40da0b-cf97-443e-9ad4-a3188d466c42)
