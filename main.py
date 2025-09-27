import cv2
from ai.detector import TrashDetector

detector = TrashDetector()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    decision, results = detector.detect(frame)

    # Annotate results with decision
    annotated = results[0].plot()
    color = (0, 255, 0) if decision == "recyclable" else (0, 0, 255)
    cv2.putText(annotated, decision.upper(), (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Smart Trashcan AI", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
