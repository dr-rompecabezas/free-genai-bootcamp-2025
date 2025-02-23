from pathlib import Path

import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class SitelenPonaRecognizer:
    def __init__(self, templates_dir='templates'):
        """Initialize with a directory of template images"""
        self.templates = {}
        self.load_templates(templates_dir)
        
    def load_templates(self, templates_dir):
        """Load template images for each character"""
        template_path = Path(templates_dir)
        for template_file in template_path.glob('*.png'):
            char_name = template_file.stem
            template = cv2.imread(str(template_file), cv2.IMREAD_GRAYSCALE)
            if template is None:
                st.error(f"Failed to load template: {template_file}")
                continue
                
            # Store preprocessed template
            processed = self.preprocess_image(template)
            self.templates[char_name] = processed
            
    def preprocess_image(self, image):
        """Preprocess image for comparison"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                        
        # Threshold to create binary image (inverted for black-on-white)
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Resize to standard size
        standard_size = (100, 100)
        resized = cv2.resize(binary, standard_size)
        
        # Find contours and center the character
        contours, _ = cv2.findContours(resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Find the main contour (largest area)
            main_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(main_contour)
            
            # Center the character
            center_x = standard_size[0] // 2
            center_y = standard_size[1] // 2
            translation_x = center_x - (x + w // 2)
            translation_y = center_y - (y + h // 2)
            
            M = np.float32([[1, 0, translation_x], [0, 1, translation_y]])
            centered = cv2.warpAffine(resized, M, standard_size)
                        
            return centered
        return resized

    def compare_images(self, img1, img2):
        """Compare two preprocessed images using a combination of template matching and contour similarity"""
        # 1. Template matching score
        result = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
        template_score = np.max(result)
        
        # 2. Contour matching score
        contours1, _ = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours1 or not contours2:
            return 0
            
        # Get main contours
        cnt1 = max(contours1, key=cv2.contourArea)
        cnt2 = max(contours2, key=cv2.contourArea)
        
        # Compare contour shapes
        match_score = cv2.matchShapes(cnt1, cnt2, cv2.CONTOURS_MATCH_I2, 0)
        # Convert to similarity score (lower distance = higher similarity)
        contour_score = 1 / (1 + match_score)
        
        # Combine scores with equal weights
        final_score = (template_score + contour_score) / 2
                
        return final_score

    def recognize(self, drawn_image, threshold=0.5):
        """Recognize drawn character by comparing with templates"""
        # Debug: Show the raw input image
        st.write("Raw input:")
        st.image(drawn_image, caption="Input Image", width=100)
        
        processed_input = self.preprocess_image(drawn_image)
        
        # Debug: Show the processed image
        st.write("After preprocessing:")
        st.image(processed_input, caption="Processed Image", width=100)
        
        best_match = None
        best_score = 0
        all_scores = {}
        
        # Compare with each template
        for char_name, template in self.templates.items():
            score = self.compare_images(processed_input, template)
            all_scores[char_name] = score
            if score > best_score:
                best_score = score
                best_match = char_name
        
        # Debug: Show all template scores
        with st.expander("View all template scores", expanded=False):
            st.write(all_scores)
        
        if best_score >= threshold:
            return best_match, best_score
        return None, best_score

def main():
    st.title("Sitelen Pona Learning App")
    
    recognizer = SitelenPonaRecognizer()
    
    # Sidebar for app navigation
    mode = st.sidebar.selectbox(
        "Choose Input Method",
        ["Draw Character", "Upload Image", "Webcam"]
    )
    
    if mode == "Draw Character":
        st.write("Draw a Sitelen Pona character:")
        canvas_result = st_canvas(
            stroke_width=8,
            stroke_color="#000",
            background_color="#fff",
            height=300,
            width=300,
            drawing_mode="freedraw",
            key="canvas",
        )
        
        if canvas_result.image_data is not None and st.button("Check Character"):
            image = canvas_result.image_data
            char, confidence = recognizer.recognize(image)
            
            if char:
                st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                # Show reference image
                st.image(recognizer.templates[char], caption=f"Reference {char}", width=100)
            else:
                st.warning(f"No match found (Best match confidence: {confidence:.2f})")
                
    elif mode == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=100)
            
            if st.button("Check Character"):
                image_array = np.array(image)
                char, confidence = recognizer.recognize(image_array)
                
                if char:
                    st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                    st.image(recognizer.templates[char], caption=f"Reference {char}", width=100)
                else:
                    st.warning(f"No match found (Best match confidence: {confidence:.2f})")
                    
    else:  # Webcam mode
        picture = st.camera_input("Take a picture")
        if picture:
            image = Image.open(picture)
            st.image(image, caption="Captured Image", width=100)
            
            if st.button("Check Character"):
                image_array = np.array(image)
                char, confidence = recognizer.recognize(image_array)
                
                if char:
                    st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                    st.image(recognizer.templates[char], caption=f"Reference {char}", width=100)
                else:
                    st.warning(f"No match found (Best match confidence: {confidence:.2f})")

if __name__ == "__main__":
    main()
