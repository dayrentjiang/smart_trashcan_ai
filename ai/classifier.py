from config import CATEGORY_MAP

class Classifier:
    def __init__(self, category_map=CATEGORY_MAP):
        self.category_map = category_map

    def decide(self, detections):
        mapped = []
        for det in detections:
            label = det["label"]
            conf = det["conf"]

            if label in self.category_map:
                mapped.append((self.category_map[label], conf))

        if not mapped:
            return "trash"  # fallback

        # Contamination rule: if any "trash" detected → trash
        if any(cat == "trash" for cat, _ in mapped):
            return "trash"

        # Otherwise pick the category with highest confidence
        return max(mapped, key=lambda x: x[1])[0]
