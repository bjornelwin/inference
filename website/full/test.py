from flask import Flask, request, render_template, jsonify
import os
app = Flask(__name__)

image_paths = []

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

@app.route('/detect_objects', methods=['GET', 'POST'])
def detect_objects():
    # Get the index parameter from the request
    index = request.json['index']

    # Your code to detect objects in the image goes here
    # You can access the image data and the index if needed
    # Perform object detection and return the results
    detected_objects = [...]  # Example: List of detected objects
    return jsonify(detected_objects)

@app.route('/get_description', methods=['POST'])
def get_description():
    # Get the index parameter from the request
    index = request.json['index']
    # Your code to get description of the image goes here
    # You can access the image data and the index if needed
    # Perform description extraction and return the results
    image_filename = os.listdir(IMAGES_FOLDER)[index]
    
    return jsonify({'description': image_filename})


if __name__ == '__main__':
    app.run(debug=True)  # Use a different port, such as 8000

