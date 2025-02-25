#!/usr/bin/env python3
import os
from pathlib import Path
import urllib.request

def download_model(model_path: str, model_url: str):
    """Download the model if it doesn't exist."""
    if not os.path.exists(model_path):
        print(f"Downloading model to {model_path}...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        urllib.request.urlretrieve(model_url, model_path)
        print("Model downloaded successfully!")
    else:
        print(f"Model already exists at {model_path}")

def main():
    # MediaPipe model URLs and paths
    models = {
        "models/mobilenet_v3_small.tflite": "https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite",
    }

    for model_path, model_url in models.items():
        download_model(model_path, model_url)

if __name__ == "__main__":
    main()
