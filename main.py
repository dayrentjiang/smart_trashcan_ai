import cv2
import time
import glob
from collections import Counter
from ai.detector import TrashDetector
from ai.classifier import Classifier
from hardware.controller import ArduinoController

NUM_SNAPSHOTS = 5
CAPTURE_DELAY = 0.1
CONF_THRESHOLD = 0.3

def auto_detect_arduino_port():
    """Automatically detect Arduino serial port on Raspberry Pi."""
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    if ports:
        print(f"[INFO] Found Arduino on {ports[0]}")
        return ports[0]
    print("[WARN] No Arduino detected automatically. Running in dummy mode.")
    return None

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
    return top[0][0].upper()

def main():
    detector = TrashDetector("best.pt", conf_threshold=CONF_THRESHOLD)
    classifier = Classifier()

    port = auto_detect_arduino_port()
    arduino = ArduinoController(port=port if port else "", dummy=(port is None))

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] ❌ Could not open camera.")
        return

    print("[INFO] Camera opened. Press ENTER to capture or Q to quit.")
    headless = True  # Set False if you are using desktop GUI

    while True:
        key = input("[ACTION] Press ENTER to capture, or 'q' to quit: ")
        if key.lower() == "q":
            break

        print("[INFO] Starting 5-frame capture...")
        decision = decide_from_snapshots(detector, classifier, cap)

        print(f"[RESULT] Final decision: {decision}")
        arduino.send(decision)

        if not headless:
            ret, frame = cap.read()
            if ret:
                cv2.putText(frame, decision, (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                            (0, 255, 0) if decision != "TRASH" else (0, 0, 255), 3)
                cv2.imshow("Smart Trashcan", frame)
                cv2.waitKey(500)

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
