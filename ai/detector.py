from ultralytics import YOLO
import config

class TrashDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        decision = "non_recyclable"

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]

                if label in config.RECYCLABLE:
                    decision = "recyclable"
                else:
                    decision = "non_recyclable"

        return decision, results
