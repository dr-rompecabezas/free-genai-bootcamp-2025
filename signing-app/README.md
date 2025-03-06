# Luka Pona Signing Learning App

Powered by MediaPipe's Hand Landmark Detection Framework.

This prototype application helps users learn sign language by comparing their hand gestures with template signs. It uses computer vision and machine learning to analyze hand movements and provide feedback on signing accuracy.

## Components

### Main Sign Comparison Engine (`main.py`)

The core comparison engine that:

- Extracts hand landmarks from GIF recordings using MediaPipe
- Normalizes hand positions to account for different hand sizes and positions
- Compares signs using Dynamic Time Warping (DTW)
- Generates detailed feedback including similarity scores and areas for improvement

### Sign Visualization Tool (`sign_visualizer.py`)

A visualization tool that:

- Displays real-time hand tracking with MediaPipe
- Creates side-by-side comparisons of template and learner signs
- Generates heatmaps showing differences in hand landmark positions
- Saves comparison animations as GIFs

## Demo

[Video demonstration will be added here]

## Requirements

- Python 3.x
- OpenCV (cv2)
- MediaPipe
- NumPy
- SciPy
- FastDTW
- Matplotlib
- Pillow
- imageio

## Running the Programs

1. To use the sign comparison engine:

    ```bash
    python main.py
    ```

    This will compare template and learner signs, providing numerical feedback and areas for improvement.

2. To use the visualization tool:

    ```python
    from sign_visualizer import SignVisualizer

    visualizer = SignVisualizer()
    visualizer.compare_signs_visually('path/to/template.gif', 'path/to/learner.gif')
    ```

    The visualizer can display real-time comparisons and generate detailed heatmaps of hand movements.
