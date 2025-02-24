import os
import urllib.request

# Create models directory if it doesn't exist
os.makedirs("../models", exist_ok=True)

# URL for the pre-converted TFLite model
model_url = "https://storage.googleapis.com/mediapipe-models/image_embedder/mobilenet_v3_small/float32/1/mobilenet_v3_small.tflite"
output_path = "../models/mobilenet_v3_small.tflite"

# Download the model
print(f"Downloading model from {model_url}...")
urllib.request.urlretrieve(model_url, output_path)
print(f"Model downloaded successfully to {output_path}!")
