import cv2
import numpy as np
from pathlib import Path
import streamlit as st
from streamlit_drawable_canvas import st_canvas


class SitelenPonaTeacher:
    def __init__(self, templates_dir="templates"):
        self.templates_dir = templates_dir
        self.templates = self.load_templates()

    def load_templates(self):
        """Load all template images"""
        templates = {}
        template_path = Path(self.templates_dir)
        for template_file in template_path.glob("*.png"):
            char_name = template_file.stem
            template = cv2.imread(str(template_file), cv2.IMREAD_GRAYSCALE)
            if template is not None:
                templates[char_name] = self.preprocess_image(template)
        return templates

    def preprocess_image(self, image):
        """Preprocess image for feature detection"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Normalize size
        image = cv2.resize(image, (100, 100))

        # Convert to binary, ensuring black strokes on white background
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

        # Find the bounding box of the content
        coords = cv2.findNonZero(binary)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)

            # Add padding
            padding = 2
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(binary.shape[1] - x, w + 2 * padding)
            h = min(binary.shape[0] - y, h + 2 * padding)

            # Crop to content
            binary = binary[y : y + h, x : x + w]

            # Resize the cropped content to standard size while maintaining aspect ratio
            if w > h:
                new_w = 80
                new_h = int(h * (80 / w))
            else:
                new_h = 80
                new_w = int(w * (80 / h))

            binary = cv2.resize(binary, (new_w, new_h))

            # Create a new centered image
            result = np.zeros((100, 100), dtype=np.uint8)
            y_offset = (100 - new_h) // 2
            x_offset = (100 - new_w) // 2
            result[y_offset : y_offset + new_h, x_offset : x_offset + new_w] = binary

            return result

        return binary

    def draw_debug_visualization(self, image, contour, centroid=None):
        """Draw contour and centroid on image for visualization"""
        # Convert grayscale to RGB for colored visualization
        vis_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Draw contour in red
        cv2.drawContours(vis_image, [contour], -1, (255, 0, 0), 2)

        # Draw centroid in green if provided
        if centroid is not None:
            cx, cy = centroid
            cv2.circle(vis_image, (int(cx), int(cy)), 5, (0, 255, 0), -1)

        return vis_image

    def analyze_drawing(self, drawn_image, target_char):
        """Analyze drawing compared to target character"""
        if target_char not in self.templates:
            return None

        # Debug: Show input images
        with st.expander("Debug: Input Images", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("Drawn Image:")
                st.image(drawn_image, caption="Raw Input", width=200)
            with col2:
                st.write("Target Template:")
                st.image(self.templates[target_char], caption="Template", width=200)

        # Preprocess drawn image
        processed_drawing = self.preprocess_image(drawn_image)
        target_template = self.templates[target_char]

        # Debug: Show preprocessed images
        with st.expander("Debug: Preprocessed Images", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("Processed Drawing:")
                st.image(processed_drawing, caption="Processed Input", width=200)
            with col2:
                st.write("Target Template:")
                st.image(target_template, caption="Template", width=200)

        # Calculate various similarity metrics
        feedback = {}

        # Find contours
        contours_drawing, _ = cv2.findContours(
            processed_drawing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours_target, _ = cv2.findContours(
            target_template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Debug: Show contour information
        with st.expander("Debug: Contour Analysis", expanded=True):
            st.write(f"Number of contours in drawing: {len(contours_drawing)}")
            st.write(f"Number of contours in template: {len(contours_target)}")

        if contours_drawing and contours_target:
            # Compare main contours
            main_contour_drawing = max(contours_drawing, key=cv2.contourArea)
            main_contour_target = max(contours_target, key=cv2.contourArea)

            # Calculate centroids
            moments_drawing = cv2.moments(main_contour_drawing)
            moments_target = cv2.moments(main_contour_target)

            drawing_centroid = None
            target_centroid = None

            if moments_drawing["m00"] != 0:
                cx_drawing = moments_drawing["m10"] / moments_drawing["m00"]
                cy_drawing = moments_drawing["m01"] / moments_drawing["m00"]
                drawing_centroid = (cx_drawing, cy_drawing)

            if moments_target["m00"] != 0:
                cx_target = moments_target["m10"] / moments_target["m00"]
                cy_target = moments_target["m01"] / moments_target["m00"]
                target_centroid = (cx_target, cy_target)

            # Debug: Show contour visualization
            with st.expander("Debug: Contour Visualization", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Drawing Contours and Centroid:")
                    vis_drawing = self.draw_debug_visualization(
                        processed_drawing, main_contour_drawing, drawing_centroid
                    )
                    st.image(vis_drawing, caption="Drawing Analysis", width=200)
                with col2:
                    st.write("Template Contours and Centroid:")
                    vis_template = self.draw_debug_visualization(
                        target_template, main_contour_target, target_centroid
                    )
                    st.image(vis_template, caption="Template Analysis", width=200)

            # Debug: Show contour areas
            with st.expander("Debug: Contour Measurements", expanded=True):
                st.write(
                    f"Drawing contour area: {cv2.contourArea(main_contour_drawing):.2f}"
                )
                st.write(
                    f"Template contour area: {cv2.contourArea(main_contour_target):.2f}"
                )

            # Shape similarity using contours and Hu moments
            similarity = cv2.matchShapes(
                main_contour_drawing, main_contour_target, cv2.CONTOURS_MATCH_I2, 0
            )
            # Debug: Show raw similarity score
            with st.expander("Debug: Shape Analysis", expanded=True):
                st.write(f"Raw matchShapes similarity score: {similarity:.6f}")

            # Based on empirical testing with Sitelen Pona glyphs:
            # similarity < 1.0 = very good match (>80%)
            # similarity 1.0-3.0 = decent match (40-80%)
            # similarity > 3.0 = poor match (<40%)

            # Use a piece-wise function for more intuitive scoring
            if similarity < 1.0:
                # Very good matches: map [0, 1] to [80%, 100%]
                shape_score = 0.8 + (0.2 * (1 - similarity))
            elif similarity < 3.0:
                # Decent matches: map [1, 3] to [40%, 80%]
                shape_score = 0.4 + (0.4 * (3 - similarity) / 2)
            else:
                # Poor matches: exponential decay for scores below 40%
                shape_score = 0.4 * np.exp(-0.3 * (similarity - 3))

            # Add more debug info about score conversion
            with st.expander("Debug: Score Conversion", expanded=True):
                st.write(f"Raw similarity: {similarity:.6f}")
                st.write(
                    f"Score category: {'Very good' if similarity < 1.0 else 'Decent' if similarity < 3.0 else 'Poor'}"
                )
                st.write(f"Final score: {shape_score:.2%}")

            feedback["shape_similarity"] = shape_score

            # Size comparison with stricter scoring
            area_drawing = cv2.contourArea(main_contour_drawing)
            area_target = cv2.contourArea(main_contour_target)
            area_ratio = min(area_drawing, area_target) / max(area_drawing, area_target)
            # Make size scoring more lenient
            size_ratio = np.sqrt(
                area_ratio
            )  # Use square root instead of square to be more lenient
            feedback["size_accuracy"] = size_ratio

            # Position analysis with normalized distance
            moments_drawing = cv2.moments(main_contour_drawing)
            moments_target = cv2.moments(main_contour_target)

            if moments_drawing["m00"] != 0 and moments_target["m00"] != 0:
                cx_drawing = moments_drawing["m10"] / moments_drawing["m00"]
                cy_drawing = moments_drawing["m01"] / moments_drawing["m00"]
                cx_target = moments_target["m10"] / moments_target["m00"]
                cy_target = moments_target["m01"] / moments_target["m00"]

                # Calculate normalized distance (as a fraction of image size)
                img_diagonal = np.sqrt(100 * 100 + 100 * 100)  # Image is 100x100
                position_error = np.sqrt(
                    (cx_drawing - cx_target) ** 2 + (cy_drawing - cy_target) ** 2
                )
                # Make position scoring more lenient
                position_score = max(
                    0, 1 - (position_error / (img_diagonal * 0.3))
                )  # Increased from 0.2 to 0.3
                feedback["position_accuracy"] = position_score

        return feedback


def main():
    st.title("Sitelen Pona Learning App")

    teacher = SitelenPonaTeacher()

    # Character selection
    available_chars = list(teacher.templates.keys())
    target_char = st.selectbox("Select character to practice:", available_chars)

    if target_char:
        # Create two columns for the reveal button and the character display
        col1, col2 = st.columns([1, 3])

        with col1:
            show_target = st.button("Reveal Target")

        with col2:
            # Only show if reveal is clicked
            if show_target:
                st.image(teacher.templates[target_char], caption=target_char, width=200)
            else:
                st.write(
                    "Character hidden - test your memory! Click 'Reveal Target' to see it."
                )

        # Drawing canvas
        st.write("Draw the character:")
        canvas_result = st_canvas(
            stroke_width=8,
            stroke_color="#000",
            background_color="#fff",
            height=300,
            width=300,
            drawing_mode="freedraw",
            key="canvas",
        )

        check_col1, check_col2 = st.columns([1, 3])
        with check_col1:
            check_button = st.button("Check Drawing")

        if canvas_result.image_data is not None and check_button:
            # Analyze drawing
            feedback = teacher.analyze_drawing(canvas_result.image_data, target_char)

            if feedback:
                # Show target character alongside feedback if it wasn't already revealed
                if not show_target:
                    st.subheader("Target Character:")
                    st.image(
                        teacher.templates[target_char], caption=target_char, width=200
                    )

                # Display feedback with visual indicators
                st.subheader("Feedback:")

                col1, col2, col3 = st.columns(3)

                with col1:
                    shape_score = feedback["shape_similarity"]
                    st.metric("Shape Similarity", f"{shape_score:.2%}")
                    if shape_score < 0.5:
                        st.write("Try to match the basic shape more closely")
                    elif shape_score < 0.8:
                        st.write("Shape is good, but could be more precise")
                    else:
                        st.write("Excellent shape matching!")

                with col2:
                    size_score = feedback["size_accuracy"]
                    st.metric("Size Accuracy", f"{size_score:.2%}")
                    if size_score < 0.5:
                        st.write("Your drawing is very different in size")
                    elif size_score < 0.8:
                        st.write("Size is close but could be more accurate")
                    else:
                        st.write("Perfect size!")

                with col3:
                    pos_score = feedback["position_accuracy"]
                    st.metric("Position Accuracy", f"{pos_score:.2%}")
                    if pos_score < 0.5:
                        st.write("Try to center your drawing better")
                    elif pos_score < 0.8:
                        st.write("Position is good but could be more centered")
                    else:
                        st.write("Excellent positioning!")

                # Overall feedback
                average_score = np.mean([shape_score, size_score, pos_score])
                st.subheader(f"Overall Score: {average_score:.2%}")

                if average_score < 0.5:
                    st.write(
                        "Keep practicing! Try to match the target character more closely."
                    )
                elif average_score < 0.8:
                    st.write("Good attempt! Focus on refining the details.")
                else:
                    st.write("Excellent work! You've mastered this character!")
                    st.balloons()


if __name__ == "__main__":
    main()
