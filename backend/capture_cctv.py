import cv2
from ultralytics import YOLO
import time

# Load your trained YOLO model
model = YOLO("model/best.pt")

# Replace this with your CCTV stream or local video path
stream_url = "test_video.mp4"   # change to your local mp4 video path for testing
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("❌ Cannot open camera stream")
    exit()

# Print model class names for debugging
print("✅ Model classes:", model.names)

print("✅ Stream started. Press 'q' to quit.\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to read frame — exiting...")
        break

    # Run YOLO model
    results = model(frame, conf=0.25, stream=False, verbose=False)

    accident_detected = False
    confidence = 0.0
    detected_classes = []

    if len(results[0].boxes) > 0:
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            detected_classes.append(label)

            # Print every detection (for debugging)
            print(f"Detected: {label} ({conf:.2f})")

            # Check if accident detected
            if label.lower() == "accident" and conf > 0.4:
                accident_detected = True
                confidence = conf
                break

    # Overlay info on frame
    label = f"Accident: {accident_detected} ({confidence:.2f})"
    cv2.putText(frame, label, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255) if accident_detected else (0, 255, 0), 2)

    cv2.imshow("CCTV Stream", frame)

    # Print in terminal
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Accident Detected: {accident_detected}, Confidence: {confidence:.2f}")
    print(f"🧾 Classes Detected: {detected_classes}\n")

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Quitting stream...")
        break

cap.release()
cv2.destroyAllWindows()
