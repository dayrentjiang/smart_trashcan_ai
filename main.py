import cv2
from ai.detector import TrashDetector

detector = TrashDetector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    decision, results, detections = detector.detect(frame)

    annotated = frame.copy()

    # Draw detection boxes
    for det in detections:
        x1, y1, x2, y2 = det["xyxy"]
        text = f"{det['label']} {det['conf']:.2f}"
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (255, 255, 255), 2)
        cv2.putText(annotated, text, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Big banner with final decision
    banner_color = (0, 255, 0) if decision == "recyclable" else (0, 0, 255)
    cv2.putText(annotated, decision.upper(), (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, banner_color, 3)

    cv2.imshow("Smart Trashcan AI (Prep Mode)", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
