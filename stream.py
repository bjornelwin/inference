from flask import Flask, render_template, Response
import cv2
from inference_models import yolo
from read_classes_and_colors import ClassesAndColors
import numpy as np

app = Flask(__name__)

model = yolo()
coco_classes, color_pans = ClassesAndColors()

def generate_frames():
    # Initialize the USB camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    # Set the width and height of the video capture
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        boxes, scores, classes = model.infer(frame)
        boxed_frame = draw_boxes(frame, boxes, scores, classes, coco_classes, color_pans)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', boxed_frame)

        # Ensure encoding was successful
        if not ret:
            continue

        # Yield the output frame in byte format
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    # Release the camera when done
    cap.release()

def draw_boxes(frame, boxes, scores, classes, class_names, color_pans):
    boxed_image = np.copy(frame)
    for i in range(len(boxes)):
        box = boxes[i]
        ymin, xmin, ymax, xmax = box
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        class_index = int(classes[i])
        class_name = class_names[class_index]
        color = color_pans[class_index % len(color_pans)]
        cv2.rectangle(boxed_image, (xmin, ymin), (xmax, ymax), color, 2)
        cv2.putText(boxed_image, f"{class_name} {scores[i]:.2f}", (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return boxed_image

@app.route('/')
def index():
    return render_template('cv2.jinja')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
