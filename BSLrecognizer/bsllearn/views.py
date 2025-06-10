from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('C:/Users/User/Desktop/Final Year Project/Code/bslweb/bsllearn/yolo_weight/12l-v5.pt')

# Home Page View
def home(request):
    # Generate A-Z alphabet (exclude H and J)
    alphabet = [chr(i) for i in range(65, 91) if chr(i) not in ['H', 'J']]
    return render(request, "home.html", {"alphabet": alphabet})

def detect_objects(frame):
    # Resize the frame to the required input size for YOLO
    resized_frame = cv2.resize(frame, (416, 416), interpolation=cv2.INTER_LINEAR)

    # detect and predict the object class in the frame
    results = model(resized_frame, device='cuda')[0]

    detection_info = None

    # Find the detection with the highest confidence
    if len(results.boxes) > 0:
        # Get all detection confidences
        confidences = results.boxes.conf.tolist()

        # Find the index of the detection with the highest confidence
        max_confidence_idx = confidences.index(max(confidences))

        # Get the detection with the highest confidence
        max_box = results.boxes[max_confidence_idx]
        

        # Get bounding box coordinates
        # x1, y1, x2, y2 = map(int, max_box.xyxy[0].tolist())

        # Get class label and confidence
        class_id = int(max_box.cls[0])
        label = model.names[class_id]
        confidence = float(max_box.conf[0])

        #Debug rectangle
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # text = f"{label} {confidence:.2f}"
        # cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Store detection info
        detection_info = {
            "label": label,
            "confidence": confidence,
        }

    # Return the frame and detection info
    return frame, detection_info

from django.http import JsonResponse

# Global variable to store detection info
detection_info_global = None

# Send the detection info to frontend with JSON format
def detection_info(request):
    global detection_info_global
    if detection_info_global:
        return JsonResponse(detection_info_global)
    else:
        return JsonResponse({"label": "None", "confidence": 0.0})

def generate_frames():
    global detection_info_global
    # Open the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect Objects in the frame
        processed_frame, detection_info_global = detect_objects(frame)

        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        if not ret:
            continue

        # Yield the frame in byte format
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Realease the webcam
    cap.release()


@gzip.gzip_page
def video_feed(request):
    # Stream the video feed
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')