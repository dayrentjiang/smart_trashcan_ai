import cv2
import time
from collections import Counter
from ai.detector import TrashDetector
from ai.classifier import Classifier
from hardware.controller import ArduinoController

NUM_SNAPSHOTS = 5
CAPTURE_DELAY = 0.1
CONF_THRESHOLD = 0.3

def decide_from_snapshots(detector, classifier, cap):
    decisions = []
    for _ in range(NUM_SNAPSHOTS):
        ret, frame = cap.read()
        if not ret:
            continue
        detections = detector.detect(frame)
        decision = classifier.decide(detections)
        decisions.append(decision)
        time.sleep(CAPTURE_DELAY)

    if not decisions:
        return "TRASH"

    top = Counter(decisions).most_common(1)[0][0]
    return top.upper()

def main():
    detector = TrashDetector("best.pt", conf_threshold=CONF_THRESHOLD)
    classifier = Classifier()
    arduino = ArduinoController(port="/dev/cu.usbserial-1110")

    cap = cv2.VideoCapture(0)
    print("[INFO] Camera opened. Waiting for IR sensor trigger...")

    try:
        while True:
            line = arduino.read_line()
            if not line:
                time.sleep(0.05)
                continue  # wait for Arduino trigger

            if line == "READY":
                print("[INFO] Object detected — capturing frames...")
                decision = decide_from_snapshots(detector, classifier, cap)

                ret, frame = cap.read()
                if ret:
                    cv2.putText(frame, decision, (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (0,255,0) if decision!="TRASH" else (0,0,255), 3)
                    cv2.imshow("Smart Trashcan", frame)
                    cv2.waitKey(1)

                arduino.send(decision)

    except KeyboardInterrupt:
        print("\n[INFO] Exiting program...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        arduino.close()

if __name__ == "__main__":
    main()
