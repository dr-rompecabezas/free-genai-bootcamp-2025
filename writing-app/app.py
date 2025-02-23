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
        """Preprocess image for comparison"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Resize to standard size
        image = cv2.resize(image, (100, 100))

        # Threshold to create binary image
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        return binary

    def analyze_drawing(self, drawn_image, target_char):
        """Analyze drawing compared to target character"""
        if target_char not in self.templates:
            return None

        # Preprocess drawn image
        processed_drawing = self.preprocess_image(drawn_image)
        target_template = self.templates[target_char]

        # Calculate various similarity metrics
        feedback = {}

        # 1. Overall shape similarity using contours
        contours_drawing, _ = cv2.findContours(
            processed_drawing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours_target, _ = cv2.findContours(
            target_template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if contours_drawing and contours_target:
            # Compare main contours
            main_contour_drawing = max(contours_drawing, key=cv2.contourArea)
            main_contour_target = max(contours_target, key=cv2.contourArea)

            # Shape similarity
            similarity = cv2.matchShapes(
                main_contour_drawing, main_contour_target, cv2.CONTOURS_MATCH_I2, 0
            )
            shape_score = 1 / (1 + similarity)  # Convert to similarity score
            feedback["shape_similarity"] = shape_score

            # Size comparison
            area_drawing = cv2.contourArea(main_contour_drawing)
            area_target = cv2.contourArea(main_contour_target)
            size_ratio = min(area_drawing, area_target) / max(area_drawing, area_target)
            feedback["size_accuracy"] = size_ratio

            # Position analysis
            moments_drawing = cv2.moments(main_contour_drawing)
            moments_target = cv2.moments(main_contour_target)

            if moments_drawing["m00"] != 0 and moments_target["m00"] != 0:
                cx_drawing = moments_drawing["m10"] / moments_drawing["m00"]
                cy_drawing = moments_drawing["m01"] / moments_drawing["m00"]
                cx_target = moments_target["m10"] / moments_target["m00"]
                cy_target = moments_target["m01"] / moments_target["m00"]

                position_error = np.sqrt(
                    (cx_drawing - cx_target) ** 2 + (cy_drawing - cy_target) ** 2
                )
                position_score = 1 - min(position_error / 50, 1)  # Normalize to 0-1
                feedback["position_accuracy"] = position_score

        return feedback


def main():
    st.title("Sitelen Pona Learning App")

    teacher = SitelenPonaTeacher()

    # Character selection
    available_chars = list(teacher.templates.keys())
    target_char = st.selectbox("Select character to practice:", available_chars)

    if target_char:
        # Show target character
        st.subheader("Target Character:")
        st.image(teacher.templates[target_char], caption=target_char, width=200)

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

        if canvas_result.image_data is not None and st.button("Check Drawing"):
            # Analyze drawing
            feedback = teacher.analyze_drawing(canvas_result.image_data, target_char)

            if feedback:
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


if __name__ == "__main__":
    main()
