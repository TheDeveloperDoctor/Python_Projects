import cv2
import mediapipe as mp
import numpy as np
import os
from deepface import DeepFace
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7, model_selection=0)  # Use lightweight model

# Directory to store registered face images
REGISTERED_FACE_DIR = "registered_faces"
os.makedirs(REGISTERED_FACE_DIR, exist_ok=True)

# Set threshold for face verification
MATCH_THRESHOLD = 0.9

def detect_and_verify_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)
    
    if results.detections:
        detection = results.detections[0]  # Process only the first detected face
        bboxC = detection.location_data.relative_bounding_box
        h, w, c = frame.shape
        x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
        
        face_crop = frame[y:y+height, x:x+width]
        if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
            face_crop = cv2.resize(face_crop, (150, 150))
            face_path = "temp_face.jpg"
            cv2.imwrite(face_path, face_crop)
            
            try:
                registered_faces = [os.path.join(REGISTERED_FACE_DIR, f) for f in os.listdir(REGISTERED_FACE_DIR) if f.endswith(".jpg")]
                if not registered_faces:
                    return "No Registered Faces", (255, 255, 0)
                
                for ref_img in registered_faces:
                    result = DeepFace.verify(face_path, ref_img, model_name="Facenet", enforce_detection=False)
                    
                    if result["verified"] and result["distance"] < MATCH_THRESHOLD:
                        return "Access Granted", (0, 255, 0)
                return "Access Denied", (0, 0, 255)
            except Exception as e:
                return f"Error: {e}", (0, 0, 255)
    
    return "No Face Detected", (255, 255, 255)

# Tkinter UI Setup
class FaceUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Unlock Test")
        
        self.label = Label(root, text="Face Unlock System", font=("Arial", 14))
        self.label.pack()
        
        self.video_label = Label(root)
        self.video_label.pack()
        
        self.status_label = Label(root, text="Status: Waiting...", font=("Arial", 12))
        self.status_label.pack()
        
        self.start_button = Button(root, text="Start Camera", command=self.start_camera)
        self.start_button.pack()
        
        self.register_button = Button(root, text="Register Face", command=self.register_face)
        self.register_button.pack()
        
        self.capture = None
        
    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.update_frame()
        
    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            status, color = detect_and_verify_face(frame)
            self.status_label.config(text=f"Status: {status}", fg=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            self.video_label.configure(image=img)
            self.video_label.image = img
        
        self.root.after(50, self.update_frame)  # Reduce CPU/GPU load
    
    def register_face(self):
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(rgb_frame)
                
                if results.detections:
                    detection = results.detections[0]
                    bboxC = detection.location_data.relative_bounding_box
                    h, w, c = frame.shape
                    x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                    
                    face_crop = frame[y:y+height, x:x+width]
                    if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                        face_crop = cv2.resize(face_crop, (150, 150))
                        face_filename = os.path.join(REGISTERED_FACE_DIR, f"registered_{len(os.listdir(REGISTERED_FACE_DIR)) + 1}.jpg")
                        cv2.imwrite(face_filename, face_crop)
                        self.status_label.config(text="Face Registered Successfully!", fg="#00ff00")
                        return
                
                self.status_label.config(text="No Face Detected for Registration", fg="#ff0000")

# Run the Application
if __name__ == "__main__":
    root = Tk()
    app = FaceUnlockApp(root)
    root.mainloop()