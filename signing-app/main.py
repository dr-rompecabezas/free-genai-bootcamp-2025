import cv2
import numpy as np
import mediapipe as mp
import imageio
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

class SignComparer:
    def __init__(self):
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def extract_landmarks_from_gif(self, gif_path):
        """Extract hand landmarks from each frame of a GIF."""
        # Read GIF
        gif = imageio.mimread(gif_path)
        
        # Process each frame
        all_frame_landmarks = []
        for frame in gif:
            # Convert RGBA to RGB if needed
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]
                
            # Process with MediaPipe
            results = self.hands.process(frame)
            
            # Extract landmarks (if hands detected)
            frame_landmarks = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get all landmarks as (x, y, z) coordinates
                    hand_points = []
                    for landmark in hand_landmarks.landmark:
                        hand_points.append([landmark.x, landmark.y, landmark.z])
                    frame_landmarks.append(hand_points)
            
            all_frame_landmarks.append(frame_landmarks)
        
        return all_frame_landmarks
    
    def normalize_landmarks(self, landmarks):
        """Normalize landmarks to make them invariant to hand size and position."""
        if not landmarks:
            return []
        
        normalized = []
        for frame_landmarks in landmarks:
            if not frame_landmarks:
                normalized.append([])
                continue
                
            frame_normalized = []
            for hand in frame_landmarks:
                # Use wrist as origin
                wrist = np.array(hand[0])
                
                # Find the scale factor (distance from wrist to middle finger MCP)
                scale = np.linalg.norm(np.array(hand[9]) - wrist)
                if scale == 0:  # Avoid division by zero
                    scale = 1
                
                # Normalize each point
                normalized_hand = [(np.array(point) - wrist) / scale for point in hand]
                frame_normalized.append(normalized_hand)
                
            normalized.append(frame_normalized)
            
        return normalized
    
    def compare_signs(self, template_gif, learner_gif):
        """Compare a template sign with a learner's attempt."""
        # Extract landmarks
        template_landmarks = self.extract_landmarks_from_gif(template_gif)
        learner_landmarks = self.extract_landmarks_from_gif(learner_gif)
        
        # Normalize landmarks
        template_norm = self.normalize_landmarks(template_landmarks)
        learner_norm = self.normalize_landmarks(learner_landmarks)
        
        # Create sequences for comparison (flatten hand landmarks)
        template_seq = []
        for frame in template_norm:
            if frame:  # If hands detected
                # Just use first hand for simplicity
                template_seq.append(np.array(frame[0]).flatten())
            else:
                template_seq.append(np.zeros(21*3))  # 21 landmarks, 3 coordinates each
                
        learner_seq = []
        for frame in learner_norm:
            if frame:  # If hands detected
                # Just use first hand for simplicity
                learner_seq.append(np.array(frame[0]).flatten())
            else:
                learner_seq.append(np.zeros(21*3))
        
        # Calculate similarity using Dynamic Time Warping
        distance, path = fastdtw(template_seq, learner_seq, dist=euclidean)
        
        # Calculate overall similarity score (0-100)
        max_distance = 21 * 3  # Maximum possible distance if all landmarks are completely off
        similarity_score = max(0, 100 - (distance / len(path) * 10))
        
        # Identify problematic frames
        frame_scores = []
        for template_idx, learner_idx in path:
            if template_idx < len(template_seq) and learner_idx < len(learner_seq):
                frame_dist = euclidean(template_seq[template_idx], learner_seq[learner_idx])
                frame_scores.append(max(0, 100 - (frame_dist * 10)))
        
        return {
            'similarity_score': similarity_score,
            'frame_scores': frame_scores,
            'dtw_path': path
        }
        
    def generate_feedback(self, comparison_results):
        """Generate feedback based on comparison results."""
        score = comparison_results['similarity_score']
        frame_scores = comparison_results['frame_scores']
        
        feedback = {
            'overall_score': score,
            'rating': self._get_rating(score),
            'weak_points': self._identify_weak_points(frame_scores)
        }
        
        return feedback
    
    def _get_rating(self, score):
        """Convert numerical score to rating."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Needs Practice"
    
    def _identify_weak_points(self, frame_scores):
        """Identify portions of the sign that need improvement."""
        if not frame_scores:
            return "Unable to identify specific areas for improvement."
            
        # Find segments with low scores
        weak_segments = []
        current_segment = {'start': 0, 'scores': []}
        
        for i, score in enumerate(frame_scores):
            current_segment['scores'].append(score)
            
            # Check if we should end this segment
            if (i == len(frame_scores) - 1 or  # Last frame
                (i > 0 and abs(score - frame_scores[i-1]) > 15)):  # Score change
                
                # Calculate average score for this segment
                avg_score = sum(current_segment['scores']) / len(current_segment['scores'])
                
                # If score is low, add to weak segments
                if avg_score < 70:
                    current_segment['end'] = i
                    current_segment['avg_score'] = avg_score
                    weak_segments.append(current_segment)
                
                # Start a new segment
                current_segment = {'start': i + 1, 'scores': []}
        
        # Generate feedback
        if not weak_segments:
            return "Your sign matches the template well throughout the entire motion."
            
        feedback = []
        for segment in weak_segments:
            segment_desc = f"Segment {segment['start']} to {segment['end']} needs improvement (score: {segment['avg_score']:.1f})"
            feedback.append(segment_desc)
            
        return feedback

# Example usage
if __name__ == "__main__":
    comparer = SignComparer()
    
    template_gif = "animated_gifs/example/template_sign.gif"
    learner_gif = "animated_gifs/example/learner_sign.gif"
    
    comparison = comparer.compare_signs(template_gif, learner_gif)
    feedback = comparer.generate_feedback(comparison)
    
    print(f"Overall Score: {feedback['overall_score']:.1f}/100")
    print(f"Rating: {feedback['rating']}")
    print("Areas for improvement:")
    if isinstance(feedback['weak_points'], list):
        for point in feedback['weak_points']:
            print(f"- {point}")
    else:
        print(f"- {feedback['weak_points']}")
