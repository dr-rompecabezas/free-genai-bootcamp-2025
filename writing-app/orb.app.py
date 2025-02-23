from pathlib import Path

import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas


def draw_matches(img1, kp1, img2, kp2, matches, good_match_ratio=0.75):
    """Draw matching features between two images"""
    try:
        # Ensure images are in the correct format
        img1_rgb = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        img2_rgb = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        
        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)
        
        # Get good matches
        max_dist = max(m.distance for m in matches) if matches else 0
        good_matches = [m for m in matches if m.distance < good_match_ratio * max_dist]
        
        # Draw matches
        img_matches = cv2.drawMatches(
            img1_rgb, kp1,
            img2_rgb, kp2,
            good_matches, None,
            matchColor=(0, 255, 0),  # Green color for matches
            singlePointColor=(255, 0, 0),  # Red color for single points
            flags=cv2.DrawMatchesFlags_DEFAULT
        )
        
        # Convert from BGR to RGB for Streamlit
        img_matches_rgb = cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB)
        
        return img_matches_rgb, len(good_matches)
    except Exception as e:
        st.error(f"Error in draw_matches: {str(e)}")
        return None, 0


class ORBSitelenPonaRecognizer:
    def __init__(self, templates_dir='templates', feature_count=100):
        """Initialize with a directory of template images"""
        self.templates_dir = templates_dir  # Store directory path
        self.raw_templates = {}  # Store raw template images
        self.processed_templates = {}  # Store processed template data
        self.initialize_orb(feature_count)
        self.load_templates()
        
    def initialize_orb(self, feature_count):
        """Initialize or reinitialize ORB detector with given feature count"""
        self.orb = cv2.ORB_create(
            nfeatures=feature_count,
            scaleFactor=1.2,
            nlevels=8,
            edgeThreshold=31,
            firstLevel=0,
            WTA_K=2,
            scoreType=cv2.ORB_HARRIS_SCORE,
            patchSize=31,
            fastThreshold=20
        )
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
    def load_templates(self):
        """Load template images and compute features"""
        template_path = Path(self.templates_dir)
        self.raw_templates = {}  # Clear existing templates
        
        # First load all raw templates
        for template_file in template_path.glob('*.png'):
            char_name = template_file.stem
            template = cv2.imread(str(template_file), cv2.IMREAD_GRAYSCALE)
            if template is None:
                st.error(f"Failed to load template: {template_file}")
                continue
            # Debug: Show the loaded template
            with st.expander(f"Loaded template: {char_name}", expanded=False):
                st.image(template, caption="Template Image", width=100)
            self.raw_templates[char_name] = template
            
        # Then process all templates
        self.process_all_templates()
    
    def process_all_templates(self):
        """Process all templates with current ORB settings"""
        self.processed_templates = {}
        for char_name, template in self.raw_templates.items():
            # Preprocess template
            processed = self.preprocess_image(template)
            
            # Compute ORB features
            kp, des = self.orb.detectAndCompute(processed, None)
            if des is not None:
                self.processed_templates[char_name] = {
                    'image': processed,
                    'keypoints': kp,
                    'descriptors': des
                }
    
    def update_feature_count(self, new_count):
        """Update feature count and recompute all templates"""
        self.initialize_orb(new_count)
        self.process_all_templates()
            
    def preprocess_image(self, image):
        """Preprocess image for feature detection"""
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Normalize size
        image = cv2.resize(image, (100, 100))
        
        # Enhance contrast
        image = cv2.equalizeHist(image)
        
        # Denoise
        image = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Ensure black text on white background
        _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        
        return binary

    def recognize(self, drawn_image, threshold=0.3, good_match_ratio=0.75):
        """Recognize drawn character by comparing with templates"""
        # Debug: Show the raw input image
        st.write("Raw input:")
        st.image(drawn_image, caption="Input Image", width=100)
        
        processed_input = self.preprocess_image(drawn_image)
        
        # Debug: Show the processed image
        st.write("After preprocessing:")
        st.image(processed_input, caption="Processed Image", width=100)
        
        # Compute ORB features for input image
        kp1, des1 = self.orb.detectAndCompute(processed_input, None)
        
        if des1 is None:
            return None, 0

        # Debug feature detection
        st.write(f"Number of keypoints in input image: {len(kp1) if kp1 else 0}")
        st.write(f"Input descriptor shape: {des1.shape if des1 is not None else 'None'}")

        best_match = None
        best_score = 0
        best_viz = None
        all_scores = {}
        
        for char_name, template_data in self.processed_templates.items():
            des2 = template_data['descriptors']
            kp2 = template_data['keypoints']
            
            # Match descriptors
            matches = self.bf.match(des1, des2)
            
            if len(matches) > 0:
                # Calculate matching score
                min_dist = min(m.distance for m in matches)
                max_dist = max(m.distance for m in matches)
                
                if max_dist == min_dist:
                    score = 0
                else:
                    # Normalize score between 0 and 1
                    good_matches = [m for m in matches if m.distance < good_match_ratio * max_dist]
                    score = len(good_matches) / len(matches)
                
                all_scores[char_name] = score
                
                if score > best_score:
                    best_score = score
                    best_match = char_name
                    # Generate visualization for best match
                    best_viz, num_good_matches = draw_matches(
                        processed_input, kp1,
                        template_data['image'], kp2,
                        matches, good_match_ratio
                    )
        
        # Debug: Show all template scores
        with st.expander("View all template scores", expanded=False):
            st.write(all_scores)

        # Show feature matches for best match if found
        if best_match and best_viz is not None:
            with st.expander("View feature matches", expanded=True):
                try:
                    # Debug information
                    st.write(f"Visualization shape: {best_viz.shape}")
                    st.write(f"Visualization dtype: {best_viz.dtype}")
                    
                    # Ensure the image is in the correct format for Streamlit
                    if best_viz.dtype != np.uint8:
                        best_viz = (best_viz * 255).astype(np.uint8)
                    
                    st.image(
                        best_viz,
                        caption=f"Feature matches with {best_match}",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error displaying matches: {str(e)}")

        if best_score >= threshold:
            return best_match, best_score
        return None, best_score

def main():
    st.title("Sitelen Pona Learning App")
    
    recognizer = ORBSitelenPonaRecognizer()
    
    # Sidebar for app navigation
    mode = st.sidebar.selectbox(
        "Choose Input Method",
        ["Draw Character", "Upload Image", "Webcam"]
    )
    
    # Add parameters to the sidebar
    st.sidebar.subheader("Recognition Parameters")
    threshold = st.sidebar.slider("Match Threshold", 0.0, 1.0, 0.3, 0.05)
    good_match_ratio = st.sidebar.slider("Good Match Ratio", 0.0, 1.0, 0.75, 0.05)
    feature_count = st.sidebar.slider("Number of Features", 50, 500, 100, 50)

    # Update feature count if it changed
    if 'last_feature_count' not in st.session_state:
        st.session_state.last_feature_count = feature_count
    elif st.session_state.last_feature_count != feature_count:
        recognizer.update_feature_count(feature_count)
        st.session_state.last_feature_count = feature_count

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
            char, confidence = recognizer.recognize(image, threshold, good_match_ratio)
            
            if char:
                st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                # Show reference image
                st.image(recognizer.processed_templates[char]['image'], caption=f"Reference {char}", width=100)
            else:
                st.warning(f"No match found (Best match confidence: {confidence:.2f})")
                
    elif mode == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=100)
            
            if st.button("Check Character"):
                image_array = np.array(image)
                char, confidence = recognizer.recognize(image_array, threshold, good_match_ratio)
                
                if char:
                    st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                    st.image(recognizer.processed_templates[char]['image'], caption=f"Reference {char}", width=100)
                else:
                    st.warning(f"No match found (Best match confidence: {confidence:.2f})")
                    
    else:  # Webcam mode
        picture = st.camera_input("Take a picture")
        if picture:
            image = Image.open(picture)
            st.image(image, caption="Captured Image", width=100)
            
            if st.button("Check Character"):
                image_array = np.array(image)
                char, confidence = recognizer.recognize(image_array, threshold, good_match_ratio)
                
                if char:
                    st.success(f"Recognized as: {char} (Confidence: {confidence:.2f})")
                    st.image(recognizer.processed_templates[char]['image'], caption=f"Reference {char}", width=100)
                else:
                    st.warning(f"No match found (Best match confidence: {confidence:.2f})")

if __name__ == "__main__":
    main()
