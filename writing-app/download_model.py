import os
import urllib.request

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# URL for the pre-converted TFLite model
model_url = "https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/1/efficientnet_lite0.tflite"
output_path = "models/efficientnet_lite0_fp32.tflite"

# Download the model
print(f"Downloading model from {model_url}...")
urllib.request.urlretrieve(model_url, output_path)
print(f"Model downloaded successfully to {output_path}!")
