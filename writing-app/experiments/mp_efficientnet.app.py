import streamlit as st
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from streamlit_drawable_canvas import st_canvas
import cv2
from pathlib import Path


class SitelenPonaRecognizer:
    def __init__(self, model_path="../models/efficientnet_lite0_fp32.tflite"):
        """Initialize the recognizer with MediaPipe"""
        # Create options for the MediaPipe Image Embedder
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ImageEmbedderOptions(
            base_options=base_options,
            quantize=True,  # Reduce memory usage
        )

        # Create the embedder
        self.embedder = vision.ImageEmbedder.create_from_options(options)

        # Load templates
        self.templates = {}
        self.template_embeddings = {}
        self.all_scores = {}
        self.load_templates()

    def load_templates(self, templates_dir="../templates"):
        """Load and compute embeddings for all template images"""
        template_path = Path(templates_dir)
        for template_file in template_path.glob("*.png"):
            char_name = template_file.stem

            # Load template image
            image = cv2.imread(str(template_file))
            self.templates[char_name] = image

            # Convert to MediaPipe Image
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            )

            # Compute and store embedding
            embedding_result = self.embedder.embed(mp_image)
            self.template_embeddings[char_name] = embedding_result.embeddings[
                0
            ].embedding

    def preprocess_image(self, image_array):
        """Preprocess image for MediaPipe"""
        # Convert RGBA to RGB
        if image_array.shape[-1] == 4:
            rgb = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        else:
            rgb = image_array

        return mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

    def compute_similarity(self, embedding1, embedding2):
        """Compute cosine similarity between embeddings"""
        # Both inputs should already be numpy arrays
        return float(
            np.dot(embedding1, embedding2)
            / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        )

    def recognize(self, drawn_image, threshold=0.7):
        """Recognize drawn character using MediaPipe embeddings"""
        # Preprocess drawn image
        processed_image = self.preprocess_image(drawn_image)

        # Get embedding for drawn image
        embedding_result = self.embedder.embed(processed_image)
        drawn_embedding = embedding_result.embeddings[0].embedding

        # Compare with all templates
        best_match = None
        best_score = 0
        self.all_scores = {}

        for char_name, template_embedding in self.template_embeddings.items():
            similarity = self.compute_similarity(drawn_embedding, template_embedding)
            self.all_scores[char_name] = similarity

            if similarity > best_score:
                best_score = similarity
                best_match = char_name

        if best_score >= threshold:
            return best_match, best_score
        return None, best_score


def main():
    st.title("Sitelen Pona Learning App")

    # Initialize recognizer
    @st.cache_resource
    def get_recognizer():
        return SitelenPonaRecognizer()

    try:
        recognizer = get_recognizer()
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.info("Make sure you have the EfficientNet Lite model file in your directory")
        return

    # Create canvas for drawing
    st.write("Draw a Sitelen Pona character:")
    canvas_result = st_canvas(
        stroke_width=8,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=300,
        width=300,
        drawing_mode="freedraw",
        key="canvas",
    )

    # Add recognition threshold slider
    threshold = st.slider("Recognition Threshold", 0.0, 1.0, 0.7, 0.05)

    if canvas_result.image_data is not None:
        # Create two columns for input and reference images
        col1, col2 = st.columns(2)

        with col1:
            st.write("Your Drawing:")
            # Convert RGBA to RGB for display
            drawn_rgb = cv2.cvtColor(canvas_result.image_data, cv2.COLOR_RGBA2RGB)
            st.image(drawn_rgb, width=200)

        if st.button("Check Character"):
            char, confidence = recognizer.recognize(
                canvas_result.image_data, threshold=threshold
            )

            with col2:
                if char:
                    st.write("Best Match:")
                    # Show reference image
                    st.image(
                        cv2.cvtColor(recognizer.templates[char], cv2.COLOR_BGR2RGB),
                        width=200,
                    )
                    st.success(f"Recognized as: {char}")
                    st.write(f"Confidence: {confidence:.3f}")
                else:
                    st.warning(f"No match found (Best confidence: {confidence:.3f})")

            # Show all scores in a collapsible section
            with st.expander("Show all similarity scores"):
                # Sort scores by value in descending order
                sorted_scores = sorted(
                    recognizer.all_scores.items(), key=lambda x: x[1], reverse=True
                )
                # Create a DataFrame for better display
                import pandas as pd

                scores_df = pd.DataFrame(
                    sorted_scores, columns=["Character", "Similarity"]
                )
                scores_df["Similarity"] = scores_df["Similarity"].round(3)
                st.dataframe(scores_df, hide_index=True)


if __name__ == "__main__":
    main()
