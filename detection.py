from ultralytics import YOLO

class Detector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, imgsz=640)[0]
        out = []
        if results.boxes is None:
            return out
        for box, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            x1, y1, x2, y2 = map(int, box.tolist())
            label = self.model.names[int(cls)]
            out.append({'bbox': (x1,y1,x2,y2), 'label': label, 'conf': float(conf)})
        return out
