from ultralytics import YOLO
import config

class TrashDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.4):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        detections = []
        found_recyclable = False
        found_non_recyclable = False

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf = float(box.conf[0])

                if conf < self.conf_threshold:
                    continue  # ignore weak predictions

                detections.append({
                    "label": label,
                    "conf": conf,
                    "xyxy": box.xyxy[0].cpu().numpy().astype(int)
                })

                if label in config.RECYCLABLE:
                    found_recyclable = True
                else:
                    found_non_recyclable = True

        # contamination rule
        if found_non_recyclable:
            decision = "non_recyclable"
        elif found_recyclable:
            decision = "recyclable"
        else:
            decision = "non_recyclable"  # fallback

        return decision, results, detections
