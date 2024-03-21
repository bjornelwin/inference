from flask import Flask, request, render_template, jsonify, Response
import os
import cv2
from inference_models import yolo
from read_classes_and_colors import ClassesAndColors
import numpy as np


app = Flask(__name__)

model = yolo()
coco_classes, color_pans = ClassesAndColors()
camera = cv2.VideoCapture(1)#'/dev/video1')

def process_text(input_text):
    # Your Python function to process the text goes here
    # For example, let's just return the input text reversed
    print(f"The text is {input_text[::-1]}")
    return f"The text is {input_text[::-1]}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['userInput']
        processed_text = process_text(user_input)
        # Return processed text wrapped in HTML tags
        return f'<div>{processed_text}</div>'
    # elif request.method == '' 
    return 'Hello, this is the homepage'

IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), 'static/data/images')

@app.route('/image_list')
def get_image_list():
    # Get a list of image filenames in the images folder
    image_files = os.listdir(IMAGES_FOLDER)
    # Create a list of image paths
    image_paths = [os.path.join('/static/data/images', filename) for filename in image_files]
    # Return the list of image paths as JSON
    return jsonify({"paths": image_paths,"descriptions": image_paths})

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

@app.route('/detect_objects', methods=['GET', 'POST'])
def detect_objects():
    # Get the index parameter from the request
    index = request.json['index']
    image_filename = os.listdir(IMAGES_FOLDER)[index]
    image_path = os.path.join(IMAGES_FOLDER, image_filename)
    # Read the image using OpenCV
    frame = cv2.imread(image_path)
    # Check if the image was successfully loaded
    if frame is None:
        return jsonify({'error': f'Failed to load image: {image_path}'})

    boxes, scores, classes = model.infer(frame)
    boxed_frame = draw_boxes(frame, boxes, scores, classes, coco_classes, color_pans)
    
    unique_classes = set(classes)
    class_list = [coco_classes[cls] for cls in unique_classes]
    
    
    annotated_folder = "website/full/static/data/annotated"
    if not os.path.exists(annotated_folder):
        os.makedirs(annotated_folder)
        
    cv2.imwrite(f"website/full/static/data/annotated/{image_filename}", boxed_frame)
    # Your code to detect objects in the image goes here
    # You can access the image data and the index if needed
    # Perform object detection and return the results
    return jsonify({"path": f"http://127.0.0.1:5000/static/data/annotated/{image_filename}", "classes": class_list})

@app.route('/get_description', methods=['POST'])
def get_description():
    # Get the index parameter from the request
    index = request.json['index']
    # Your code to get description of the image goes here
    # You can access the image data and the index if needed
    # Perform description extraction and return the results
    image_filename = os.listdir(IMAGES_FOLDER)[index]
    
    return jsonify({'description': image_filename})

def generate_frames():
    start_image = False
    while True:
        # Read the camera frame
        success, frame = camera.read()
        if not success:
            if not start_image:
                print("Error reading frame:", frame)

                image_filename = os.listdir(IMAGES_FOLDER)[2]
                image_path = os.path.join(IMAGES_FOLDER, image_filename)
                # Read the image using OpenCV
                frame = cv2.imread(image_path)
                boxes, scores, classes = model.infer(frame) 
                frame = draw_boxes(frame, boxes, scores, classes, coco_classes, color_pans)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                start_image = True
            else:
                break
            
        else:
            boxes, scores, classes = model.infer(frame) 
            frame = draw_boxes(frame, boxes, scores, classes, coco_classes, color_pans)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()
    
@app.route('/')
def index2():
    return render_template('cv2.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)  # Use a different port, such as 8000




