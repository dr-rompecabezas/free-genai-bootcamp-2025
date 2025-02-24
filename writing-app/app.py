import cv2
import numpy as np
from pathlib import Path
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
from PIL import Image
import math


class MobileNetSitelenPonaRecognizer:
    def __init__(
        self, templates_dir="templates", model_path="models/mobilenet_v3_small.tflite"
    ):
        """Initialize with a directory of template images and download model"""
        self.templates_dir = templates_dir
        self.templates = {}
        self.embeddings = {}

        # Initialize MediaPipe Image Embedder with proper options
        base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
        options = mp.tasks.vision.ImageEmbedderOptions(
            base_options=base_options,
            l2_normalize=True,  # Enable L2 normalization for better similarity comparison
        )
        self.embedder = mp.tasks.vision.ImageEmbedder.create_from_options(options)

        self.load_templates()

    def download_and_load_model(self, model_path):
        """Download and load the MobileNetV3 TFLite model using MediaPipe"""
        try:
            # Download model if not already present
            if not Path(model_path).exists():
                model_url = "https://storage.googleapis.com/mediapipe-assets/mobile_net_v3_small_224_224_quant.tflite"
                urllib.request.urlretrieve(model_url, model_path)

            # Create MediaPipe Image Embedder with proper options
            base_options = python.BaseOptions(model_asset_path=model_path)
            options = vision.ImageEmbedderOptions(
                base_options=base_options,
                l2_normalize=True,  # Important for cosine similarity
                quantize=True,
            )
            self.embedder = vision.ImageEmbedder.create_from_options(options)
        except Exception as e:
            st.error(f"Failed to load model: {str(e)}")
            raise

    def preprocess_image(self, image):
        """Preprocess image for MediaPipe"""
        # Convert to RGB if needed
        if len(image.shape) == 3:
            if image.shape[2] == 4:  # RGBA
                # For canvas input, properly handle alpha channel
                mask = image[:, :, 3] > 0  # Get mask of non-transparent pixels
                rgb = image[:, :, :3]
                # Set transparent pixels to white (background color)
                white_bg = np.ones_like(rgb) * 255
                rgb = np.where(mask[:, :, None], rgb, white_bg)
                image = rgb
            elif image.shape[2] == 3:  # BGR
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif len(image.shape) == 2:  # Grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Resize while maintaining aspect ratio
        target_size = (224, 224)  # MobileNet default size
        h, w = image.shape[:2]
        aspect = w / h

        if aspect > 1:
            new_w = target_size[0]
            new_h = int(new_w / aspect)
        else:
            new_h = target_size[1]
            new_w = int(new_h * aspect)

        resized = cv2.resize(image, (new_w, new_h))

        # Create white canvas of target size (since we're dealing with black text)
        canvas = np.ones((target_size[1], target_size[0], 3), dtype=np.uint8) * 255

        # Center the image on the canvas
        y_offset = (target_size[1] - new_h) // 2
        x_offset = (target_size[0] - new_w) // 2
        canvas[y_offset : y_offset + new_h, x_offset : x_offset + new_w] = resized

        # Normalize pixel values to [0, 1]
        processed = canvas.astype(np.float32) / 255.0

        return processed

    def get_embedding(self, image):
        """Get embedding from preprocessed image using MediaPipe"""
        try:
            # Preprocess and create MediaPipe image
            processed = self.preprocess_image(image)

            # For debugging, return the processed image too
            debug_image = (processed * 255).astype(np.uint8)

            # Convert to uint8 for MediaPipe (it doesn't like float input)
            mp_input = (processed * 255).astype(np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_input)

            # Get embedding
            embedding_result = self.embedder.embed(mp_image)

            # Return the embedding values (already a numpy array) and debug image
            return embedding_result.embeddings[0].embedding, debug_image
        except Exception as e:
            st.error(f"Failed to get embedding: {str(e)}")
            raise

    def load_templates(self):
        """Load and process all template images"""
        template_path = Path(self.templates_dir)
        for template_file in template_path.glob("*.png"):
            char_name = template_file.stem

            # Load and preprocess the image
            original = cv2.imread(str(template_file))
            original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
            processed = self.preprocess_image(original)

            # Store images for display
            self.templates[char_name] = {
                "original": original,
                "processed": (processed * 255).astype(np.uint8),
            }

            # Convert to uint8 for MediaPipe (it doesn't like float input)
            mp_input = (processed * 255).astype(np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_input)

            # Get and store embedding values
            embedding_result = self.embedder.embed(mp_image)
            self.embeddings[char_name] = embedding_result.embeddings[0].embedding

    def cosine_similarity(self, a, b):
        """Calculate cosine similarity between two embeddings"""
        # Debug print the shapes and first few values
        st.write("Debug - Embedding shapes:", a.shape, b.shape)
        st.write("Debug - First few values of a:", a[:5])
        st.write("Debug - First few values of b:", b[:5])

        # Embeddings should already be L2 normalized due to embedder options
        # Just compute dot product for cosine similarity
        similarity = float(np.dot(a, b))
        st.write("Debug - Raw similarity score:", similarity)

        return similarity

    def recognize(self, drawn_image, threshold=0.7):
        """Recognize drawn character using MobileNetV3 embeddings"""
        # Preprocess input image
        processed_input = self.preprocess_image(drawn_image)

        # Get embedding for input
        input_embedding, debug_image = self.get_embedding(processed_input)

        if input_embedding is None:
            return None, 0

        # Compare with all templates
        best_match = None
        best_score = 0
        all_scores = {}

        for char_name, template_embedding in self.embeddings.items():
            # Calculate similarity score
            score = self.cosine_similarity(input_embedding, template_embedding)
            all_scores[char_name] = float(score)

            if score > best_score:
                best_score = score
                best_match = char_name

        # Debug: Show all scores
        with st.expander("View all similarity scores", expanded=False):
            st.write(all_scores)

        if best_score >= threshold:
            return best_match, best_score
        return None, best_score


def main():
    st.title("Sitelen Pona Learning App (MobileNetV3)")

    recognizer = MobileNetSitelenPonaRecognizer()

    # Sidebar for app navigation and parameters
    mode = st.sidebar.selectbox(
        "Choose Input Method", ["Draw Character", "Upload Image", "Webcam"]
    )

    # Character selection
    available_chars = sorted(recognizer.templates.keys())
    selected_char = st.sidebar.selectbox(
        "Select Character to Practice", available_chars
    )

    # Show the template for the selected character
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Template Reference")
        show_template = st.button("Show Template")
        template_container = st.empty()
        if show_template:
            template_container.image(
                recognizer.templates[selected_char]["original"], width=200
            )
            if st.button("Hide Template"):
                template_container.empty()

    with col2:
        st.subheader("Practice Area:")
        if mode == "Draw Character":
            canvas_result = st_canvas(
                stroke_width=4,  # Thinner stroke for better detail
                stroke_color="#000",
                background_color="#fff",
                height=224,  # Match model input size
                width=224,  # Match model input size
                drawing_mode="freedraw",
                key="canvas",
            )

            if canvas_result.image_data is not None and st.button("Check My Drawing"):
                try:
                    # Get embedding and debug image for drawn character
                    drawn_embedding, drawn_debug = recognizer.get_embedding(
                        canvas_result.image_data
                    )

                    # Get template info
                    template_debug = recognizer.templates[selected_char]["processed"]
                    template_embedding = recognizer.embeddings[selected_char]

                    # Show debug information
                    st.subheader("Debug Information")

                    # Show processed images side by side
                    debug_col1, debug_col2 = st.columns(2)
                    with debug_col1:
                        st.write("Processed Template:")
                        st.image(template_debug, width=150)
                    with debug_col2:
                        st.write("Processed Drawing:")
                        st.image(drawn_debug, width=150)

                    # Compare embeddings
                    confidence = recognizer.cosine_similarity(
                        drawn_embedding, template_embedding
                    )

                    # Show embedding analysis
                    with st.expander("Embedding Analysis"):
                        st.write("Template Embedding Stats:")
                        st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                        st.write(f"- Std: {np.std(template_embedding):.4f}")
                        st.write(f"- Min: {np.min(template_embedding):.4f}")
                        st.write(f"- Max: {np.max(template_embedding):.4f}")

                        st.write("\nDrawing Embedding Stats:")
                        st.write(f"- Mean: {np.mean(drawn_embedding):.4f}")
                        st.write(f"- Std: {np.std(drawn_embedding):.4f}")
                        st.write(f"- Min: {np.min(drawn_embedding):.4f}")
                        st.write(f"- Max: {np.max(drawn_embedding):.4f}")

                    # Show final score with more detail
                    st.subheader("Recognition Result")
                    if confidence >= 0.7:
                        st.success(f"Great job! Similarity score: {confidence:.4f}")
                    elif confidence >= 0.5:
                        st.warning(f"Getting there! Similarity score: {confidence:.4f}")
                    else:
                        st.error(f"Keep practicing! Similarity score: {confidence:.4f}")

                except Exception as e:
                    st.error(f"Error processing drawing: {str(e)}")

        elif mode == "Upload Image":
            uploaded_file = st.file_uploader(
                "Upload your practice image...", type=["png", "jpg", "jpeg"]
            )
            if uploaded_file is not None:
                image = cv2.imdecode(
                    np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR
                )
                st.image(image, caption="Uploaded Image", width=300)

                if st.button("Check My Image"):
                    try:
                        # Get embedding and debug image for uploaded image
                        uploaded_embedding, uploaded_debug = recognizer.get_embedding(
                            image
                        )

                        # Get template info
                        template_debug = recognizer.templates[selected_char][
                            "processed"
                        ]
                        template_embedding = recognizer.embeddings[selected_char]

                        # Show debug information
                        st.subheader("Debug Information")

                        # Show processed images side by side
                        debug_col1, debug_col2 = st.columns(2)
                        with debug_col1:
                            st.write("Processed Template:")
                            st.image(template_debug, width=150)
                        with debug_col2:
                            st.write("Processed Uploaded Image:")
                            st.image(uploaded_debug, width=150)

                        # Compare embeddings
                        confidence = recognizer.cosine_similarity(
                            uploaded_embedding, template_embedding
                        )

                        # Show embedding analysis
                        with st.expander("Embedding Analysis"):
                            st.write("Template Embedding Stats:")
                            st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                            st.write(f"- Std: {np.std(template_embedding):.4f}")
                            st.write(f"- Min: {np.min(template_embedding):.4f}")
                            st.write(f"- Max: {np.max(template_embedding):.4f}")

                            st.write("\nUploaded Image Embedding Stats:")
                            st.write(f"- Mean: {np.mean(uploaded_embedding):.4f}")
                            st.write(f"- Std: {np.std(uploaded_embedding):.4f}")
                            st.write(f"- Min: {np.min(uploaded_embedding):.4f}")
                            st.write(f"- Max: {np.max(uploaded_embedding):.4f}")

                        # Show final score with more detail
                        st.subheader("Recognition Result")
                        if confidence >= 0.7:
                            st.success(f"Great job! Similarity score: {confidence:.4f}")
                        elif confidence >= 0.5:
                            st.warning(
                                f"Getting there! Similarity score: {confidence:.4f}"
                            )
                        else:
                            st.error(
                                f"Keep practicing! Similarity score: {confidence:.4f}"
                            )
                    except Exception as e:
                        st.error(f"Error processing image: {str(e)}")

        elif mode == "Webcam":
            picture = st.camera_input("Take a picture of your drawing")
            if picture is not None:
                image = cv2.imdecode(
                    np.frombuffer(picture.read(), np.uint8), cv2.IMREAD_COLOR
                )

                if st.button("Check My Picture"):
                    try:
                        # Get embedding and debug image for captured image
                        captured_embedding, captured_debug = recognizer.get_embedding(
                            image
                        )

                        # Get template info
                        template_debug = recognizer.templates[selected_char][
                            "processed"
                        ]
                        template_embedding = recognizer.embeddings[selected_char]

                        # Show debug information
                        st.subheader("Debug Information")

                        # Show processed images side by side
                        debug_col1, debug_col2 = st.columns(2)
                        with debug_col1:
                            st.write("Processed Template:")
                            st.image(template_debug, width=150)
                        with debug_col2:
                            st.write("Processed Captured Image:")
                            st.image(captured_debug, width=150)

                        # Compare embeddings
                        confidence = recognizer.cosine_similarity(
                            captured_embedding, template_embedding
                        )

                        # Show embedding analysis
                        with st.expander("Embedding Analysis"):
                            st.write("Template Embedding Stats:")
                            st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                            st.write(f"- Std: {np.std(template_embedding):.4f}")
                            st.write(f"- Min: {np.min(template_embedding):.4f}")
                            st.write(f"- Max: {np.max(template_embedding):.4f}")

                            st.write("\nCaptured Image Embedding Stats:")
                            st.write(f"- Mean: {np.mean(captured_embedding):.4f}")
                            st.write(f"- Std: {np.std(captured_embedding):.4f}")
                            st.write(f"- Min: {np.min(captured_embedding):.4f}")
                            st.write(f"- Max: {np.max(captured_embedding):.4f}")

                        # Show final score with more detail
                        st.subheader("Recognition Result")
                        if confidence >= 0.7:
                            st.success(f"Great job! Similarity score: {confidence:.4f}")
                        elif confidence >= 0.5:
                            st.warning(
                                f"Getting there! Similarity score: {confidence:.4f}"
                            )
                        else:
                            st.error(
                                f"Keep practicing! Similarity score: {confidence:.4f}"
                            )
                    except Exception as e:
                        st.error(f"Error processing picture: {str(e)}")

    # Add some helpful tips
    with st.expander("Tips for Better Recognition"):
        st.markdown("""
        - Draw the character as similar to the template as possible
        - Make sure your drawing is centered
        - Use clear, bold strokes
        - Try to maintain similar proportions to the template
        """)


if __name__ == "__main__":
    main()
