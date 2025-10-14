from ultralytics import YOLO

class TrashDetector:
    def __init__(self, model_path="best.pt", conf_threshold=0.4):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []

        for r in results: 
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < self.conf_threshold:
                    continue

                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                xyxy = box.xyxy[0].cpu().numpy().astype(int)  # (x1,y1,x2,y2)

                detections.append({
                    "label": label,
                    "conf": conf,
                    "xyxy": xyxy
                })

        return detections
