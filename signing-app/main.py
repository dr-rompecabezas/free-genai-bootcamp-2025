import cv2
import numpy as np
import imageio
from PIL import Image
import mediapipe as mp


def gif_to_numpy_array(gif_path):
    """
    Convert an animated GIF to a list of numpy arrays.
    
    Args:
        gif_path (str): Path to the GIF file
        
    Returns:
        list: List of numpy arrays, each representing a frame in BGR format (OpenCV format)
    """
    # Read the GIF file using imageio
    gif = imageio.mimread(gif_path)
    
    # Convert each frame to a numpy array in BGR format (for OpenCV)
    frames = []
    for frame in gif:
        # Convert RGBA to RGB if needed
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]
        
        # Convert RGB to BGR (OpenCV format)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frames.append(frame_bgr)
    
    return frames


def process_gif_with_mediapipe(gif_path):
    """
    Process each frame of a GIF with MediaPipe Hand Landmark Detector.
    
    Args:
        gif_path (str): Path to the GIF file
    """
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # Convert GIF to frames
    frames = gif_to_numpy_array(gif_path)
    
    # Process each frame with MediaPipe
    results_list = []
    for i, frame in enumerate(frames):
        # Convert the BGR image to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe
        results = hands.process(frame_rgb)
        
        # Store results
        results_list.append(results)
        
        # Visualize (optional)
        if results.multi_hand_landmarks:
            # Create a copy of the frame for visualization
            annotated_frame = frame.copy()
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )
            
            # Display annotated frame
            cv2.imshow(f'Frame {i}', annotated_frame)
            cv2.waitKey(100)  # Display each frame for 100ms
    
    # Clean up
    hands.close()
    cv2.destroyAllWindows()
    
    return results_list

# Example usage
if __name__ == "__main__":
    gif_path = "animated_gifs/ike.gif"
    results = process_gif_with_mediapipe(gif_path)
    
    # Now you can work with the MediaPipe results for each frame
    print(f"Processed {len(results)} frames")
