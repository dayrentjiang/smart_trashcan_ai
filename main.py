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
    for i in range(NUM_SNAPSHOTS):
        ret, frame = cap.read()
        if not ret:
            continue
        detections = detector.detect(frame)
        decision = classifier.decide(detections)
        decisions.append(decision)
        time.sleep(CAPTURE_DELAY)

    if not decisions:
        return "TRASH"

    if "trash" in decisions:
        return "TRASH"

    c = Counter(decisions)
    top = c.most_common()
    if len(top) == 1 or top[0][1] > top[1][1]:
        return top[0][0].upper()
    else:
        return top[0][0].upper()

def main():
    detector = TrashDetector("best.pt", conf_threshold=CONF_THRESHOLD)
    classifier = Classifier()
    arduino = ArduinoController(port="/dev/cu.usbserial-1110")

    cap = cv2.VideoCapture(0)
    print("[INFO] Camera opened. Press ENTER to capture or Q to quit.")

    while True:
        key = input("[ACTION] Press ENTER to simulate detection, or 'q' to quit: ")
        if key.lower() == "q":
            break

        print("[INFO] Starting 5-frame capture...")
        decision = decide_from_snapshots(detector, classifier, cap)

        # show preview frame with decision
        ret, frame = cap.read()
        if ret:
            cv2.putText(frame, decision, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (0,255,0) if decision!="TRASH" else (0,0,255), 3)
            cv2.imshow("Smart Trashcan", frame)
            cv2.waitKey(1)

        arduino.send(decision)

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()


if __name__ == "__main__":
    main()
