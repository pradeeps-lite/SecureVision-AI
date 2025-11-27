import os
import cv2
import face_recognition

KNOWN_DIR = "backend/known_faces"

class FaceManager:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []
        self.load_known()

    def load_known(self):
        if not os.path.exists(KNOWN_DIR):
            os.makedirs(KNOWN_DIR)
        for name in os.listdir(KNOWN_DIR):
            person_dir = os.path.join(KNOWN_DIR, name)
            if os.path.isdir(person_dir):
                for fname in os.listdir(person_dir):
                    img = face_recognition.load_image_file(os.path.join(person_dir, fname))
                    enc = face_recognition.face_encodings(img)
                    if enc:
                        self.known_encodings.append(enc[0])
                        self.known_names.append(name)

    def recognize(self, roi):
        try:
            rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            enc = face_recognition.face_encodings(rgb)
            if not enc:
                return "Unknown"
            matches = face_recognition.compare_faces(self.known_encodings, enc[0], tolerance=0.5)
            if True in matches:
                return self.known_names[matches.index(True)]
            return "Unknown"
        except Exception:
            return "Unknown"

    def save_face(self, img_bytes, name):
        import io, numpy as np
        image = face_recognition.load_image_file(io.BytesIO(img_bytes))
        person_dir = os.path.join(KNOWN_DIR, name)
        os.makedirs(person_dir, exist_ok=True)
        count = len(os.listdir(person_dir))
        save_path = os.path.join(person_dir, f"{name}_{count+1}.jpg")
        cv2.imwrite(save_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        self.known_encodings = []
        self.known_names = []
        self.load_known()
