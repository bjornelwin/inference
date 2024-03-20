from flask import Flask, render_template
import os

app = Flask(__name__)

# Define the path to the images folder
IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), '/home/bjorn/inference/data/images')

@app.route('/')
def index():
    # Get a list of image filenames in the images folder
    image_files = os.listdir(IMAGES_FOLDER)
    # Create a list of image paths
    image_paths = [os.path.join('/home/bjorn/inference/data/images', filename) for filename in image_files]
    # Render the HTML template and pass the image paths to it
    print(image_paths)
    return render_template('m.html', image_paths=image_paths)

if __name__ == '__main__':
    app.run(debug=True)
