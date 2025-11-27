# SecureVision AI

SecureVision AI is a real-time intelligent surveillance system that performs:
- Object / threat detection (YOLO-based)
- Face recognition (face_recognition)
- AI-generated / deepfake face heuristic detection (LBP + optional deep models)
- Secure web dashboard with real-time video, alerts, and logs

This repository contains a modular full-stack starter you can extend for internships, demos, and research.

## Quickstart (local)

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### With Docker
```bash
docker-compose up --build
```

Author: Pradeep Sathapathi
