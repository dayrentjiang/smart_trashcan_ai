import cv2
import time
import requests
import threading
from collections import Counter
from ai.detector import TrashDetector
from ai.classifier import Classifier
from hardware.controller import ArduinoController

NUM_SNAPSHOTS = 5
CAPTURE_DELAY = 0.1
CONF_THRESHOLD = 0.3
API_URL = "https://smart-trashcan-server.onrender.com/api/trash/update"

def send_to_server(category, frame):
    """Send category and image to the server asynchronously"""
    try:
        # Save frame temporarily
        temp_image = f"temp_trash_{int(time.time())}.jpg"
        cv2.imwrite(temp_image, frame)
        
        # Prepare multipart form data
        with open(temp_image, 'rb') as img_file:
            files = {
                'image': ('trash.jpg', img_file, 'image/jpeg')
            }
            data = {
                'category': category.lower()
            }
            
            # Send POST request with timeout
            response = requests.post(API_URL, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"[API] ✅ Sent to server: {result}")
            return result
        else:
            print(f"[API] ❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"[API] ❌ Failed to send to server: {e}")
        return None

def send_to_server_async(category, frame):
    """Wrapper to send data in background thread"""
    thread = threading.Thread(target=send_to_server, args=(category, frame))
    thread.daemon = True  # Thread will close when main program exits
    thread.start()
    print(f"[API] 📤 Sending to server in background...")

def decide_from_snapshots(detector, classifier, cap):
    decisions = []
    frames = []
    
    for _ in range(NUM_SNAPSHOTS):
        ret, frame = cap.read()
        if not ret:
            continue
        detections = detector.detect(frame)
        decision = classifier.decide(detections)
        decisions.append(decision)
        frames.append(frame.copy())
        time.sleep(CAPTURE_DELAY)

    if not decisions:
        return "TRASH", None

    top = Counter(decisions).most_common(1)[0][0]
    best_frame = frames[len(frames)//2] if frames else None
    return top.upper(), best_frame

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
                continue

            if line == "READY":
                print("[INFO] Object detected — capturing frames...")
                decision, best_frame = decide_from_snapshots(detector, classifier, cap)

                if best_frame is not None:
                    display_frame = best_frame.copy()
                    cv2.putText(display_frame, decision, (30, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (0,255,0) if decision!="TRASH" else (0,0,255), 3)
                    cv2.imshow("Smart Trashcan", display_frame)
                    cv2.waitKey(1)

                    # Send to server asynchronously (non-blocking)
                    print(f"[INFO] Triggering async upload: {decision}")
                    send_to_server_async(decision, best_frame)

                # Send to Arduino immediately (don't wait for upload)
                arduino.send(decision)
                print(f"[INFO] ✅ Arduino notified: {decision}")

    except KeyboardInterrupt:
        print("\n[INFO] Exiting program...")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        arduino.close()

if __name__ == "__main__":
    main()