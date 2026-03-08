"""
HerdSense Vision Server — YOLOv8 real-time behavior classification.
Run from backend directory (with venv activated):
     pip install ultralytics flask flask-cors opencv-python
     python vision_server.py
Then open the Vision tab in the app; stream at http://localhost:5001/video_feed
"""
from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
from ultralytics import YOLO
import threading
import time
import json
import os

app = Flask(__name__)
CORS(app)

# Load YOLOv8 model (downloads automatically on first run)
# Use custom trained model if available, otherwise default
model_path = "custom_trained_model.pt" if os.path.exists("custom_trained_model.pt") else "yolov8n.pt"
model = YOLO(model_path)

def _default_results(camera_ok=True):
    return {
        "behavior": "Standing" if camera_ok else "Camera unavailable",
        "confidence": 0.91 if camera_ok else 0.0,
        "risk": "LOW",
        "alert": None if camera_ok else "Grant Terminal camera access in System Settings → Privacy & Security → Camera, then restart the vision server.",
        "detections": 0,
        "timestamp": time.time(),
        "camera_available": camera_ok,
    }


def _make_placeholder_frame():
    """Return a 640x480 BGR image with 'Camera unavailable' text."""
    import numpy as np
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (40, 40, 40)
    cv2.putText(
        img, "Camera unavailable",
        (120, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 200, 200), 2
    )
    cv2.putText(
        img, "Grant Terminal camera access: System Settings -> Privacy -> Camera",
        (40, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1
    )
    return img


latest_results = None  # set below after camera check

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
camera_available = cap.isOpened() and cap.read()[0]
# Placeholder frame when camera fails (so /video_feed still sends something)
placeholder_frame = None
if not camera_available:
    place = cv2.imread("placeholder_camera.png") if os.path.exists("placeholder_camera.png") else None
    if place is None:
        place = _make_placeholder_frame()
    _, buf = cv2.imencode(".jpg", place)
    placeholder_frame = buf.tobytes()
output_frame = placeholder_frame if not camera_available else None
latest_results = _default_results(camera_available)
lock = threading.Lock()

# Prefer MPS on Apple Silicon, fallback to CPU
try:
    import torch
    device = "mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available() else "cpu"
except Exception:
    device = "cpu"


def classify_behavior(detections):
    """Map YOLO detections to cattle-style behaviors for demo."""
    if not detections:
        return "No animal detected", 0.0, "LOW"
    behaviors = []
    for det in detections:
        label = det["label"]
        conf = det["confidence"]
        box = det["box"]
        width = box[2] - box[0]
        height = box[3] - box[1]
        aspect_ratio = width / height if height > 0 else 1
        
        # Map synthetic dataset classes to cattle behaviors
        if label == "cow_eating":
            behaviors.append(("Grazing", conf, "LOW"))
        elif label == "cow_walking":
            behaviors.append(("Standing/Walking", conf, "LOW"))
        elif label == "cow_lying_down":
            behaviors.append(("Lying Down", conf, "MEDIUM"))
        elif label == "cow_standing":
            behaviors.append(("Standing", conf, "LOW"))
        elif label == "cow_distress":
            behaviors.append(("Abnormal Gait", conf, "HIGH"))
        elif label == "cow_abnormal_movement":
            behaviors.append(("Abnormal Gait", conf, "HIGH"))
        else:
            behaviors.append((f"Detected: {label}", conf, "LOW"))
    
    return behaviors[0] if behaviors else ("No animal detected", 0.0, "LOW")


def process_frames():
    global output_frame, latest_results
    if not camera_available:
        while True:
            time.sleep(1)
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        try:
            results = model(frame, verbose=False, device=device)
        except Exception:
            results = model(frame, verbose=False, device="cpu")
        detections = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls]
                xyxy = box.xyxy[0].tolist()
                cv2.rectangle(
                    frame,
                    (int(xyxy[0]), int(xyxy[1])),
                    (int(xyxy[2]), int(xyxy[3])),
                    (0, 255, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    f"{label} {conf:.2f}",
                    (int(xyxy[0]), int(xyxy[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2,
                )
                detections.append({"label": label, "confidence": conf, "box": xyxy})
        behavior, confidence, risk = classify_behavior(detections)
        alert = None
        if risk == "HIGH":
            alert = f"Abnormal behavior detected — {behavior}"
        elif behavior == "Lying Down" and confidence > 0.7:
            alert = "Extended lying detected — possible health concern"
        with lock:
            latest_results = {
                "behavior": behavior,
                "confidence": round(confidence, 2),
                "risk": risk,
                "alert": alert,
                "detections": len(detections),
                "timestamp": time.time(),
                "camera_available": True,
            }
            _, buffer = cv2.imencode(".jpg", frame)
            output_frame = buffer.tobytes()
        time.sleep(0.05)


def generate_frames():
    global output_frame
    while True:
        with lock:
            frame = output_frame
        if frame is not None:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
        time.sleep(0.05)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/results")
def get_results():
    with lock:
        return jsonify(latest_results)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    thread = threading.Thread(target=process_frames, daemon=True)
    thread.start()
    print("Vision server running on http://localhost:5001")
    print("Video feed: http://localhost:5001/video_feed")
    app.run(host="0.0.0.0", port=5001, debug=False, threaded=True)
