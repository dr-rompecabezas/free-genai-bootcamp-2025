import os
from pathlib import Path
import random
import urllib.request

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas


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
        """Compute cosine similarity between two embeddings"""
        # Embeddings should already be L2 normalized due to embedder options
        # Just compute dot product for cosine similarity
        similarity = float(np.dot(a, b))

        # Return raw similarity score
        return similarity

    def recognize(self, drawn_image, threshold=0.7):
        """Recognize drawn character by comparing embeddings"""
        # Get embedding for drawn image
        input_embedding, debug_image = self.get_embedding(drawn_image)

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

        # Store scores for debug display
        self.all_scores = all_scores

        if best_score >= threshold:
            return best_match, best_score
        return None, best_score


def main():
    st.title("Sitelen Pona Writing Practice")

    # Initialize session state for settings if not exists
    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False
    if "threshold" not in st.session_state:
        st.session_state.threshold = 0.7
    if "show_reference" not in st.session_state:
        st.session_state.show_reference = True
    if "reference_button_key" not in st.session_state:
        st.session_state.reference_button_key = 0
    if "selected_char" not in st.session_state:
        # Initialize with a random character
        available_chars = sorted(os.listdir("sitelen_pona_svgs"))
        available_chars = [
            f[:-4] for f in available_chars if f.endswith(".svg")
        ]  # remove .svg
        st.session_state.selected_char = random.choice(available_chars)

    def toggle_reference():
        st.session_state.show_reference = not st.session_state.show_reference
        st.session_state.reference_button_key += 1

    # Main app
    recognizer = MobileNetSitelenPonaRecognizer()

    # Initialize glyph color preference in session state if not present
    if "white_glyphs" not in st.session_state:
        st.session_state.white_glyphs = False

    # Get all SVG files (strip _dark suffix for naming)
    svg_files = []
    for f in os.listdir("sitelen_pona_svgs"):
        if f.endswith(".svg"):
            name = f[:-4]  # remove .svg
            svg_files.append(name)
    svg_files.sort()

    # Create tabs for main content
    tab_practice, tab_learn = st.tabs(["Practice", "Learn"])

    with tab_learn:
        st.header("Sitelen Pona Glyphs")

        # Add glyph color toggle
        use_white_glyphs = st.toggle(
            "Use white glyphs",
            value=st.session_state.white_glyphs,
            key="white_glyphs",
            help="Switch between black and white glyphs",
        )
        st.write("")  # Add some spacing

        # Create a grid layout
        cols_per_row = 8
        for i in range(0, len(svg_files), cols_per_row):
            row = svg_files[i : i + cols_per_row]
            cols = st.columns(cols_per_row)
            for j, glyph_name in enumerate(row):
                with cols[j]:
                    # Create a container for each glyph
                    with st.container():
                        # Construct SVG path with _dark suffix if needed
                        if use_white_glyphs:
                            svg_path = f"sitelen_pona_svgs_dark/{glyph_name}_dark.svg"
                        else:
                            svg_path = f"sitelen_pona_svgs/{glyph_name}.svg"

                        st.image(svg_path, width=60)
                        st.caption(glyph_name)

    with tab_practice:
        # Character selection in main area
        available_chars = sorted(recognizer.templates.keys())
        
        # Create two columns with 2:1 ratio
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_char = st.selectbox(
                "Select Character to Practice",
                available_chars,
                index=available_chars.index(st.session_state.selected_char),
                help="Choose a Sitelen Pona character to practice writing",
                key="char_selector",
            )
        
        with col2:
            # Create empty space to push button to bottom
            st.write("")
            if st.button("🎲 Random", help="Select a random character to practice"):
                st.session_state.selected_char = random.choice(available_chars)
                # Rerun to update the selectbox with the new random selection
                st.rerun()
        
        st.session_state.selected_char = selected_char

        # Sidebar settings
        with st.sidebar:
            # Input method selection
            mode = st.selectbox(
                "Choose Input Method", ["Draw Character", "Upload Image", "Webcam"]
            )

            st.divider()

            # Settings section
            st.subheader("Settings")

            # Practice settings
            st.write("**Practice Settings**")
            st.session_state.show_reference = st.toggle(
                "Show Reference by Default",
                value=st.session_state.show_reference,
                help="When disabled, reference will be hidden until you click 'Show Reference'",
            )

            # Recognition settings
            st.write("**Recognition Settings**")
            st.session_state.threshold = st.slider(
                "Recognition Threshold",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.threshold,
                step=0.05,
                help="Lower values are more lenient, higher values require more precise matches",
            )

            # Debug settings
            st.write("**Developer Options**")
            st.session_state.debug_mode = st.toggle(
                "Debug Mode",
                value=st.session_state.debug_mode,
                help="Show detailed information about image processing and recognition",
            )

            st.divider()

            # Tips section
            st.markdown("""
            ### Tips
            1. Draw in the center of the canvas
            2. Use clear, deliberate strokes
            3. Try to match the template size
            """)

        # Main content area
        col1, col2 = st.columns([2, 1])

        with col1:
            if mode == "Draw Character":
                st.subheader("Practice Area:")
                # Canvas for drawing
                canvas_result = st_canvas(
                    stroke_width=4,
                    stroke_color="#000000",
                    background_color="#FFFFFF",
                    height=224,
                    width=224,
                    drawing_mode="freedraw",
                    key="canvas",
                )
            elif mode == "Upload Image":
                st.subheader("Upload Area:")
                # File uploader
                uploaded_file = st.file_uploader(
                    "Upload an image", type=["png", "jpg", "jpeg"]
                )
                if uploaded_file is not None:
                    # Display uploaded image preview
                    image = cv2.imdecode(
                        np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR
                    )
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(image_rgb, width=224, caption="Preview")
                    if st.button("Check My Image"):
                        try:
                            # Get embedding and debug image for uploaded image
                            uploaded_embedding, uploaded_debug = recognizer.get_embedding(
                                image
                            )

                            # Get template info
                            template_debug = recognizer.templates[selected_char]["processed"]
                            template_embedding = recognizer.embeddings[selected_char]

                            # Compare embeddings
                            confidence = recognizer.cosine_similarity(
                                uploaded_embedding, template_embedding
                            )

                            # Show recognition result first
                            st.subheader("Recognition Result")
                            if confidence >= st.session_state.threshold:
                                st.success(f"Great job! Similarity score: {confidence:.4f}")
                            elif confidence >= st.session_state.threshold * 0.7:
                                st.warning(f"Getting there! Similarity score: {confidence:.4f}")
                            else:
                                st.error(f"Keep practicing! Similarity score: {confidence:.4f}")

                            # Only show debug information if debug mode is enabled
                            if st.session_state.debug_mode:
                                with st.expander("Debug Information", expanded=True):
                                    # Show embedding shapes and raw values
                                    st.write("Embedding Analysis:")
                                    st.write(
                                        f"Embedding shapes: {uploaded_embedding.shape}, {template_embedding.shape}"
                                    )

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("First few values of uploaded embedding:")
                                        st.write(uploaded_embedding[:5])
                                    with col2:
                                        st.write("First few values of template embedding:")
                                        st.write(template_embedding[:5])

                                    st.write(f"Raw similarity score: {confidence}")

                                    # Show processed images side by side
                                    st.write("Processed Images Comparison:")
                                    debug_col1, debug_col2 = st.columns(2)
                                    with debug_col1:
                                        st.write("Template:")
                                        st.image(template_debug, width=150)
                                    with debug_col2:
                                        st.write("Uploaded Image:")
                                        st.image(uploaded_debug, width=150)

                                    # Show embedding statistics
                                    st.write("Embedding Statistics:")
                                    stats_col1, stats_col2 = st.columns(2)
                                    with stats_col1:
                                        st.write("Template Stats:")
                                        st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                                        st.write(f"- Std: {np.std(template_embedding):.4f}")
                                        st.write(f"- Min: {np.min(template_embedding):.4f}")
                                        st.write(f"- Max: {np.max(template_embedding):.4f}")
                                    with stats_col2:
                                        st.write("Uploaded Image Stats:")
                                        st.write(f"- Mean: {np.mean(uploaded_embedding):.4f}")
                                        st.write(f"- Std: {np.std(uploaded_embedding):.4f}")
                                        st.write(f"- Min: {np.min(uploaded_embedding):.4f}")
                                        st.write(f"- Max: {np.max(uploaded_embedding):.4f}")

                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")
            else:  # Webcam mode
                st.subheader("Capture Area:")
                picture = st.camera_input("Take a picture of your drawing")
                if picture is not None:
                    # Display captured image preview
                    image = cv2.imdecode(
                        np.frombuffer(picture.read(), np.uint8), cv2.IMREAD_COLOR
                    )
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(image_rgb, width=224, caption="Preview")
                    if st.button("Check My Picture"):
                        try:
                            # Get embedding and debug image for captured image
                            captured_embedding, captured_debug = recognizer.get_embedding(
                                image
                            )

                            # Get template info
                            template_debug = recognizer.templates[selected_char]["processed"]
                            template_embedding = recognizer.embeddings[selected_char]

                            # Compare embeddings
                            confidence = recognizer.cosine_similarity(
                                captured_embedding, template_embedding
                            )

                            # Show recognition result first
                            st.subheader("Recognition Result")
                            if confidence >= st.session_state.threshold:
                                st.success(f"Great job! Similarity score: {confidence:.4f}")
                            elif confidence >= st.session_state.threshold * 0.7:
                                st.warning(f"Getting there! Similarity score: {confidence:.4f}")
                            else:
                                st.error(f"Keep practicing! Similarity score: {confidence:.4f}")

                            # Only show debug information if debug mode is enabled
                            if st.session_state.debug_mode:
                                with st.expander("Debug Information", expanded=True):
                                    # Show embedding shapes and raw values
                                    st.write("Embedding Analysis:")
                                    st.write(
                                        f"Embedding shapes: {captured_embedding.shape}, {template_embedding.shape}"
                                    )

                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write("First few values of captured embedding:")
                                        st.write(captured_embedding[:5])
                                    with col2:
                                        st.write("First few values of template embedding:")
                                        st.write(template_embedding[:5])

                                    st.write(f"Raw similarity score: {confidence}")

                                    # Show processed images side by side
                                    st.write("Processed Images Comparison:")
                                    debug_col1, debug_col2 = st.columns(2)
                                    with debug_col1:
                                        st.write("Template:")
                                        st.image(template_debug, width=150)
                                    with debug_col2:
                                        st.write("Captured Image:")
                                        st.image(captured_debug, width=150)

                                    # Show embedding statistics
                                    st.write("Embedding Statistics:")
                                    stats_col1, stats_col2 = st.columns(2)
                                    with stats_col1:
                                        st.write("Template Stats:")
                                        st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                                        st.write(f"- Std: {np.std(template_embedding):.4f}")
                                        st.write(f"- Min: {np.min(template_embedding):.4f}")
                                        st.write(f"- Max: {np.max(template_embedding):.4f}")
                                    with stats_col2:
                                        st.write("Captured Image Stats:")
                                        st.write(f"- Mean: {np.mean(captured_embedding):.4f}")
                                        st.write(f"- Std: {np.std(captured_embedding):.4f}")
                                        st.write(f"- Min: {np.min(captured_embedding):.4f}")
                                        st.write(f"- Max: {np.max(captured_embedding):.4f}")

                        except Exception as e:
                            st.error(f"Error processing picture: {str(e)}")

        with col2:
            # Template display with visibility control
            st.subheader("Reference:")

            # Show reference if enabled
            if st.session_state.show_reference:
                st.image(
                    recognizer.templates[selected_char]["original"],
                    width=200,
                    caption=f"Template for '{selected_char}'",
                )

            # Dynamic toggle button with unique key
            button_label = (
                "Hide Reference"
                if st.session_state.show_reference
                else "Show Reference"
            )
            st.button(
                button_label,
                type="primary",
                key=f"ref_toggle_{st.session_state.reference_button_key}",
                on_click=toggle_reference,
            )

        # Results and Debug Container
        if mode == "Draw Character":
            if canvas_result.image_data is not None and st.button("Check My Drawing"):
                try:
                    # Get embedding and debug image
                    drawn_embedding, drawn_debug = recognizer.get_embedding(
                        canvas_result.image_data
                    )
                    template_debug = recognizer.templates[selected_char]["processed"]
                    template_embedding = recognizer.embeddings[selected_char]
                    confidence = recognizer.cosine_similarity(
                        drawn_embedding, template_embedding
                    )

                    # Show recognition result first
                    st.subheader("Recognition Result")
                    if confidence >= st.session_state.threshold:
                        st.success(f"Great job! Similarity score: {confidence:.4f}")
                    elif confidence >= st.session_state.threshold * 0.7:
                        st.warning(f"Getting there! Similarity score: {confidence:.4f}")
                    else:
                        st.error(f"Keep practicing! Similarity score: {confidence:.4f}")

                    # Only show debug information if debug mode is enabled
                    if st.session_state.debug_mode:
                        with st.expander("Debug Information", expanded=True):
                            # Show embedding shapes and raw values
                            st.write("Embedding Analysis:")
                            st.write(
                                f"Embedding shapes: {drawn_embedding.shape}, {template_embedding.shape}"
                            )

                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("First few values of drawn embedding:")
                                st.write(drawn_embedding[:5])
                            with col2:
                                st.write("First few values of template embedding:")
                                st.write(template_embedding[:5])

                            st.write(f"Raw similarity score: {confidence}")

                            # Show processed images side by side
                            st.write("Processed Images Comparison:")
                            debug_col1, debug_col2 = st.columns(2)
                            with debug_col1:
                                st.write("Drawing:")
                                st.image(drawn_debug, width=150)
                            with debug_col2:
                                st.write("Template:")
                                st.image(template_debug, width=150)

                            # Show embedding statistics
                            st.write("Embedding Statistics:")
                            stats_col1, stats_col2 = st.columns(2)
                            with stats_col1:
                                st.write("Template Stats:")
                                st.write(f"- Mean: {np.mean(template_embedding):.4f}")
                                st.write(f"- Std: {np.std(template_embedding):.4f}")
                                st.write(f"- Min: {np.min(template_embedding):.4f}")
                                st.write(f"- Max: {np.max(template_embedding):.4f}")
                            with stats_col2:
                                st.write("Drawing Stats:")
                                st.write(f"- Mean: {np.mean(drawn_embedding):.4f}")
                                st.write(f"- Std: {np.std(drawn_embedding):.4f}")
                                st.write(f"- Min: {np.min(drawn_embedding):.4f}")
                                st.write(f"- Max: {np.max(drawn_embedding):.4f}")

                except Exception as e:
                    st.error(f"Error processing drawing: {str(e)}")


if __name__ == "__main__":
    main()
