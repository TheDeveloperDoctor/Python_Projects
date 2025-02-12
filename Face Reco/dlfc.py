import cv2
import mediapipe as mp
import numpy as np
import os
import threading
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import face_recognition

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7, model_selection=0)  # Lightweight model

# Directory to store registered face encodings
REGISTERED_FACE_DIR = "registered_faces"
os.makedirs(REGISTERED_FACE_DIR, exist_ok=True)

# Load known face encodings
known_face_encodings = []
known_face_labels = []

# Load registered faces
for file in os.listdir(REGISTERED_FACE_DIR):
    if file.endswith(".jpg"):
        image = face_recognition.load_image_file(os.path.join(REGISTERED_FACE_DIR, file))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_labels.append(file)

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
        self.thread_running = False

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.thread_running = True
        threading.Thread(target=self.update_frame, daemon=True).start()
        
    def update_frame(self):
        while self.thread_running:
            ret, frame = self.capture.read()
            if ret:
                status, color = self.detect_and_verify_face(frame)
                self.status_label.config(text=f"Status: {status}", fg=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.video_label.configure(image=img)
                self.video_label.image = img
        
    def detect_and_verify_face(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)
        
        if results.detections:
            detection = results.detections[0]  # Process only the first detected face
            bboxC = detection.location_data.relative_bounding_box
            h, w, c = frame.shape
            x, y, width, height = (
                                        int(bboxC.xmin * w),
                                        int(bboxC.ymin * h),  # This was missing
                                        int(bboxC.width * w),
                                        int(bboxC.height * h),
                                    )

            
            face_crop = frame[y:y+height, x:x+width]
            if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                face_crop = cv2.resize(face_crop, (100, 100))
                face_encoding = face_recognition.face_encodings(face_crop)
                
                if not face_encoding:
                    return "No Face Detected", (255, 255, 255)
                
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
                if True in matches:
                    return "Access Granted", (0, 255, 0)
                return "Access Denied", (255, 0, 0)
        
        return "No Face Detected", (255, 255, 255)
    
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
                    x, y, width, height = (
                                        int(bboxC.xmin * w),
                                        int(bboxC.ymin * h),  # Add this missing line
                                        int(bboxC.width * w),
                                        int(bboxC.height * h),
                                    )

                    
                    face_crop = frame[y:y+height, x:x+width]
                    if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                        face_crop = cv2.resize(face_crop, (100, 100))
                        face_filename = os.path.join(REGISTERED_FACE_DIR, f"registered_{len(os.listdir(REGISTERED_FACE_DIR)) + 1}.jpg")
                        cv2.imwrite(face_filename, face_crop)
                        self.status_label.config(text="Face Registered Successfully!", fg="#00ff00")
                        
                        # Update known faces
                        image = face_recognition.load_image_file(face_filename)
                        encoding = face_recognition.face_encodings(image)
                        if encoding:
                            known_face_encodings.append(encoding[0])
                            known_face_labels.append(face_filename)
                        return
                
                self.status_label.config(text="No Face Detected for Registration", fg="#ff0000")

# Run the Application
if __name__ == "__main__":
    root = Tk()
    app = FaceUnlockApp(root)
    root.mainloop()
