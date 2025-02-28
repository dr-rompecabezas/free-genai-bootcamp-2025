import cv2
import numpy as np
import mediapipe as mp
import imageio
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

class SignVisualizer:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def extract_frames_with_landmarks(self, gif_path):
        """Extract frames and landmarks from a GIF file."""
        # Read GIF
        gif = imageio.mimread(gif_path)
        
        # Process each frame
        processed_frames = []
        landmarks_data = []
        
        for frame in gif:
            # Convert RGBA to RGB if needed
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]
            
            # Convert to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Create a copy for drawing on
            annotated_frame = frame_bgr.copy()
            
            # Process with MediaPipe
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            
            # Store landmark data
            frame_landmarks = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Extract landmarks
                    hand_points = []
                    for landmark in hand_landmarks.landmark:
                        hand_points.append([landmark.x, landmark.y, landmark.z])
                    frame_landmarks.append(hand_points)
                    
                    # Draw landmarks on the frame
                    self.mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
            
            # Convert back to RGB for display
            annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            processed_frames.append(annotated_frame_rgb)
            landmarks_data.append(frame_landmarks)
        
        return processed_frames, landmarks_data
    
    def display_frames(self, frames, title="Hand Tracking Visualization"):
        """Display frames as an animation."""
        fig, ax = plt.figure(figsize=(10, 6)), plt.gca()
        ax.set_title(title)
        ax.axis('off')
        
        # Display the first frame
        img_display = ax.imshow(frames[0])
        
        # Animation function
        def update(frame_num):
            img_display.set_array(frames[frame_num])
            return [img_display]
        
        # Create animation
        ani = FuncAnimation(fig, update, frames=len(frames), interval=100, blit=True)
        plt.show()
        
        return ani
    
    def compare_signs_visually(self, template_gif, learner_gif):
        """Compare template and learner signs with visualization."""
        # Extract frames and landmarks
        template_frames, template_landmarks = self.extract_frames_with_landmarks(template_gif)
        learner_frames, learner_landmarks = self.extract_frames_with_landmarks(learner_gif)
        
        # Create a side-by-side comparison
        max_frames = max(len(template_frames), len(learner_frames))
        comparison_frames = []
        
        # Choose a common size for both frames
        target_height = 400
        target_width = 600
        
        for i in range(max_frames):
            # Get template frame or create blank
            if i < len(template_frames):
                template_frame = template_frames[i]
                # Resize template frame
                template_frame = cv2.resize(template_frame, (target_width, target_height), 
                                           interpolation=cv2.INTER_AREA)
            else:
                template_frame = np.zeros((target_height, target_width, 3), dtype=np.uint8)
            
            # Get learner frame or create blank
            if i < len(learner_frames):
                learner_frame = learner_frames[i]
                # Resize learner frame
                learner_frame = cv2.resize(learner_frame, (target_width, target_height), 
                                          interpolation=cv2.INTER_AREA)
            else:
                learner_frame = np.zeros((target_height, target_width, 3), dtype=np.uint8)
            
            # Create side-by-side frame
            comparison_frame = np.zeros((target_height, target_width*2, 3), dtype=np.uint8)
            comparison_frame[:, :target_width] = template_frame
            comparison_frame[:, target_width:] = learner_frame
            
            # Add labels
            cv2.putText(comparison_frame, "Template", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(comparison_frame, "Learner", (target_width + 10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Add frame number
            cv2.putText(comparison_frame, f"Frame: {i+1}/{max_frames}", (10, target_height-20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            comparison_frames.append(comparison_frame)
        
        return comparison_frames
    
    def save_comparison_gif(self, comparison_frames, output_path):
        """Save the comparison frames as a GIF."""
        imageio.mimsave(output_path, comparison_frames, duration=0.1)
        return output_path
    
    def display_landmark_heatmap(self, template_landmarks, learner_landmarks):
        """Display a heatmap of landmark differences between template and learner."""
        # Ensure both sequences have the same length
        min_frames = min(len(template_landmarks), len(learner_landmarks))
        
        # Calculate differences for each frame
        differences = []
        
        for i in range(min_frames):
            # Skip frames without detected hands
            if not template_landmarks[i] or not learner_landmarks[i]:
                continue
                
            # Get first hand from each frame
            template_hand = np.array(template_landmarks[i][0])
            learner_hand = np.array(learner_landmarks[i][0])
            
            # Calculate Euclidean distance for each landmark
            frame_diffs = []
            for j in range(21):  # 21 landmarks per hand
                dist = np.linalg.norm(template_hand[j] - learner_hand[j])
                frame_diffs.append(dist)
                
            differences.append(frame_diffs)
        
        # Convert to numpy array
        if differences:
            diff_array = np.array(differences)
            
            # Create heatmap
            plt.figure(figsize=(12, 8))
            plt.imshow(diff_array, aspect='auto', cmap='viridis')
            plt.colorbar(label='Euclidean Distance')
            plt.xlabel('Landmark Index')
            plt.ylabel('Frame')
            plt.title('Landmark Difference Heatmap')
            
            # Add landmark names
            landmark_names = [
                'WRIST', 'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
                'INDEX_MCP', 'INDEX_PIP', 'INDEX_DIP', 'INDEX_TIP',
                'MIDDLE_MCP', 'MIDDLE_PIP', 'MIDDLE_DIP', 'MIDDLE_TIP',
                'RING_MCP', 'RING_PIP', 'RING_DIP', 'RING_TIP',
                'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
            ]
            plt.xticks(range(21), landmark_names, rotation=90)
            
            plt.tight_layout()
            plt.show()
        else:
            print("Not enough data to create heatmap")

# Example usage
if __name__ == "__main__":
    visualizer = SignVisualizer()
    
    template_gif = "animated_gifs/example/template_sign.gif"
    learner_gif = "animated_gifs/example/learner_attempt.gif"
    
    # Display individual sign with landmarks
    print("Processing template sign...")
    template_frames, template_landmarks = visualizer.extract_frames_with_landmarks(template_gif)
    visualizer.display_frames(template_frames, "Template Sign")
    
    print("Processing learner sign...")
    learner_frames, learner_landmarks = visualizer.extract_frames_with_landmarks(learner_gif)
    visualizer.display_frames(learner_frames, "Learner Sign")
    
    # Create side-by-side comparison
    print("Creating comparison visualization...")
    comparison_frames = visualizer.compare_signs_visually(template_gif, learner_gif)
    
    # Save and display comparison
    output_gif = "comparison.gif"
    visualizer.save_comparison_gif(comparison_frames, output_gif)
    print(f"Comparison saved to {output_gif}")
    
    # Display comparison
    visualizer.display_frames(comparison_frames, "Template vs Learner")
    
    # Show difference heatmap
    visualizer.display_landmark_heatmap(template_landmarks, learner_landmarks)