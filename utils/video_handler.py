import cv2
from ultralytics import YOLO
from config import CAMERA_SOURCE, CONFIDENCE_THRESHOLD, ENABLE_LIVE_DISPLAY
from utils.logger import setup_logger
from tts.tts_engine import speak_text_live  # Importing from tts_engine for compatibility
from tts.color_correction import correct_white_balance


# Setup logger
logger = setup_logger("object_detection", "logs/project.log")

# Load YOLOv8x model
model = YOLO("yolov8x.pt")


def detect_and_display():
    cap = cv2.VideoCapture(CAMERA_SOURCE)

    if not cap.isOpened():
        logger.error("Failed to open video source.")
        return

    logger.info("Video capture started.")

    last_spoken = None  # To prevent repeating the same description

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.warning("Frame capture failed, exiting.")
                break
            
            # Correct white balance
            frame = correct_white_balance(frame)

            # Run object detection
            results = model(frame)[0]

            detected_objects = []

            for box in results.boxes:
                conf = box.conf.item()
                cls = int(box.cls.item())
                label = model.model.names[cls]

                if conf >= CONFIDENCE_THRESHOLD:
                    # Draw bounding box
                    xyxy = box.xyxy[0].tolist()
                    x1, y1, x2, y2 = map(int, xyxy)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    text = f"{label} {conf:.2f}"
                    cv2.putText(frame, text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    detected_objects.append(label)

            # Speak detected objects in descriptive format
            if detected_objects:
                unique_labels = list(set(detected_objects))
                if len(unique_labels) == 1:
                    description = f"[Image Description]: a {unique_labels[0]}"
                else:
                    joined = ", ".join(unique_labels[:-1]) + " and " + unique_labels[-1]
                    description = f"[Image Description]: {joined}"

                if description != last_spoken:
                    speak_text_live(description)
                    last_spoken = description

            # Show video
            if ENABLE_LIVE_DISPLAY:
                cv2.imshow("YOLOv8x Object Detection", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("User exited via 'q' key.")
                break

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Exiting.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Video capture ended and resources released.")
