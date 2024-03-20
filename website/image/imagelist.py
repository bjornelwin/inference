from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Define the path to the images folder
IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), 'static/data/images')

@app.route('/')
def index():
    # Get a list of image filenames in the images folder
    image_files = os.listdir(IMAGES_FOLDER)
    # Create a list of image paths
    image_paths = [os.path.join('data/images', filename) for filename in image_files]
    # Pass the list of image paths to the HTML template
    return render_template('main.html', image_paths=image_paths)

@app.route('/image_list')
def get_image_list():
    # Get a list of image filenames in the images folder
    image_files = os.listdir(IMAGES_FOLDER)
    # Create a list of image paths
    image_paths = [os.path.join('/data/images', filename) for filename in image_files]
    # Return the list of image paths as JSON
    return jsonify(image_paths)

if __name__ == '__main__':
    app.run(debug=True)
