import cv2
import time
import os
import numpy as np
from deepface import DeepFace

class FaceVerifier:
    """
    FaceVerifier class to verify a person's identity in a video
    against an ID image using DeepFace.
    
    Attributes:
    - id_path (str): Path to the ID image.
    - threshold (float): Similarity threshold for verification.
    - id_embedding (list): Face embedding from the ID image.
    """
    
    def __init__(self, id_path, threshold=0.5):
        """
        Initializes the FaceVerifier object with the ID image path
        and similarity threshold.
        Parameters:
        - id_path (str): Path to the ID image.
        - threshold (float): Similarity threshold for verification.
        """
        self.id_path = id_path
        self.threshold = threshold
        self.id_embedding = self.get_embedding(id_path)

    def get_embedding(self, image_path):
        """Extract face embedding using DeepFace."""
        try:
            embedding = DeepFace.represent(img_path=image_path, model_name="Facenet")[0]["embedding"]
            return embedding
        except:
            print(f" No face detected in {image_path}")
            return None

    def convert_blob_to_mp4(self, blob_bytes):
        """Convert a Blob byte stream into an MP4 file."""
        video_path = "converted_video.mp4"
        try:
            np_array = np.frombuffer(blob_bytes, np.uint8)
            video = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            if video is None:
                print("Error: Failed to decode blob video.")
                return None

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            height, width, _ = video.shape
            out = cv2.VideoWriter(video_path, fourcc, 20.0, (width, height))

            out.write(video)
            out.release()
            return video_path
        except Exception as e:
            print(f"Error in converting Blob to MP4: {e}")
            return None

    def verify_video(self, video_source):
        """
        Verify if the person in the video matches the ID image.
        Handles both file path and Blob input.
        """
        if self.id_embedding is None:
            return False  # ID image does not contain a face

        # Convert Blob to MP4 if necessary
        video_path = video_source
        if isinstance(video_source, bytes):  # If Blob input
            video_path = self.convert_blob_to_mp4(video_source)
            if video_path is None:
                return False  # Conversion failed

        video_capture = cv2.VideoCapture(video_path)
        start_time = time.time()
        matched = False

        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break  # Exit if video ends

            # Save current frame temporarily
            temp_frame_path = "temp_frame.jpg"
            cv2.imwrite(temp_frame_path, frame)

            try:
                # Get face embedding from the frame
                frame_embedding = DeepFace.represent(img_path=temp_frame_path, model_name="Facenet")[0]["embedding"]

                # Compare embeddings using cosine distance
                similarity = DeepFace.verify(img1_path=self.id_path, img2_path=temp_frame_path, model_name="Facenet")["distance"]

                if similarity < self.threshold:
                    matched = True
                    break  # Stop once a match is found

            except:
                pass  # No face detected in this frame, continue checking

            if time.time() - start_time > 20:  # Stop after 20 seconds
                break

        video_capture.release()
        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)  # Clean up temporary file

        return matched  # Return True if a match is found, otherwise False
