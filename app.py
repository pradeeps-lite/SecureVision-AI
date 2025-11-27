import time
import jwt
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import cv2
from models.detection import Detector
from models.face_utils import FaceManager
from utils.ai_face_detector import is_ai_generated_face

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'change_this_secret'

detector = Detector()
face_manager = FaceManager()
camera = cv2.VideoCapture(0)

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    if data.get('username') and data.get('password'):
        token = jwt.encode({'user': data['username'], 'exp': time.time()+3600}, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Bad credentials'}), 401

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        small = cv2.resize(frame, (640, 360))
        detections = detector.detect(small)
        for det in detections:
            x1,y1,x2,y2 = det['bbox']
            roi = small[y1:y2, x1:x2]
            name = face_manager.recognize(roi)
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            ai_flag = is_ai_generated_face(gray)
            label = f"{name} {'[AI]' if ai_flag else ''}"
            color = (0,255,0) if not ai_flag else (0,0,255)
            cv2.rectangle(small, (x1,y1), (x2,y2), color, 2)
            cv2.putText(small, label, (x1, max(y1-10,10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        ret, buffer = cv2.imencode('.jpg', small)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/api/stream')
@token_required
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/register_face', methods=['POST'])
@token_required
def register_face():
    if 'image' not in request.files or 'name' not in request.form:
        return jsonify({'message':'Invalid request'}), 400
    img = request.files['image'].read()
    name = request.form['name']
    face_manager.save_face(img, name)
    return jsonify({'message':'saved'}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
