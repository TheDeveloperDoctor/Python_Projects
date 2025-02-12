import cv2
import numpy as np
import os
import threading
import pickle
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import face_recognition
from sklearn import neighbors

# Load OpenCV DNN Face Detector (Res10 SSD Model)
FACE_DETECTOR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(FACE_DETECTOR_PATH)

# Directory to store registered face encodings
REGISTERED_FACE_DIR = "registered_faces"
os.makedirs(REGISTERED_FACE_DIR, exist_ok=True)

# Load known face encodings
known_face_encodings = []
known_face_labels = []

# Load KNN model
MODEL_PATH = "face_knn_model.pkl"
def train_knn_model():
    if len(known_face_encodings) > 0:
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors=3, algorithm='ball_tree', weights='distance')
        knn_clf.fit(known_face_encodings, known_face_labels)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(knn_clf, f)

def load_knn_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

# Preload registered faces
for file in os.listdir(REGISTERED_FACE_DIR):
    if file.endswith(".jpg"):
        image = face_recognition.load_image_file(os.path.join(REGISTERED_FACE_DIR, file))
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_labels.append(file)

# Train the model initially
train_knn_model()

class FaceUnlockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Unlock System")
        
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
        self.frame_skip = 3
        self.frame_counter = 0

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.thread_running = True
        threading.Thread(target=self.update_frame, daemon=True).start()
        
    def update_frame(self):
        while self.thread_running:
            ret, frame = self.capture.read()
            if ret:
                self.frame_counter += 1
                if self.frame_counter % self.frame_skip == 0:
                    status, color = self.detect_and_verify_face(frame)
                    self.status_label.config(text=f"Status: {status}", fg=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                self.video_label.configure(image=img)
                self.video_label.image = img
    
    def detect_and_verify_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_crop = frame[y:y+h, x:x+w]

            if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                face_crop = cv2.resize(face_crop, (100, 100))
                face_encoding = face_recognition.face_encodings(face_crop)

                if not face_encoding:
                    return "No Face Detected", (255, 255, 255)

                knn_clf = load_knn_model()
                if knn_clf:
                    prediction = knn_clf.predict([face_encoding[0]])
                    self.update_training_data(face_encoding[0], prediction[0])
                    return f"Access Granted: {prediction[0]}", (0, 255, 0)
        
        return "Access Denied", (255, 0, 0)
    
    def register_face(self):
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_crop = frame[y:y+h, x:x+w]

                    if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                        face_crop = cv2.resize(face_crop, (100, 100))
                        face_filename = os.path.join(REGISTERED_FACE_DIR, f"registered_{len(os.listdir(REGISTERED_FACE_DIR)) + 1}.jpg")
                        cv2.imwrite(face_filename, face_crop)
                        self.status_label.config(text="Face Registered Successfully!", fg="#00ff00")

                        image = face_recognition.load_image_file(face_filename)
                        encoding = face_recognition.face_encodings(image)
                        if encoding:
                            self.update_training_data(encoding[0], face_filename)
                            return
                
                self.status_label.config(text="No Face Detected for Registration", fg="#ff0000")
    
    def update_training_data(self, new_encoding, label):
        known_face_encodings.append(new_encoding)
        known_face_labels.append(label)
        train_knn_model()

if __name__ == "__main__":
    root = Tk()
    app = FaceUnlockApp(root)
    root.mainloop()
