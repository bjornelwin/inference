import os
import sqlite3
import numpy as np
from sklearn.neighbors import NearestNeighbors
from PIL import Image
import pytesseract
from transformers import AutoTokenizer, AutoModel
import torch

class ImageDatabase:
    def __init__(self, db_name='image_search.db'):
        self.db_name = db_name
        # Call the create_database method to create tables if not exists
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS image_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT,
                text_data TEXT,
                vector BLOB
            )
        ''')
        conn.commit()
        conn.close()

    # Function to insert data into the database
    def insert_data(self, image_path, text_data, vector):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('INSERT INTO image_data (image_path, text_data, vector) VALUES (?, ?, ?)', (image_path, text_data, vector))
        conn.commit()
        conn.close()

    # Function to retrieve all data vectors from the database
    def get_data_vectors(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT vector FROM image_data')
        vectors = c.fetchall()
        conn.close()
        return [np.frombuffer(vector[0]) for vector in vectors]

    # Step 1: Text to Vector
    def text_to_vector(self, sentence, model_name='bert-base-uncased'):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
        tokens = tokenizer(sentence, return_tensors='pt')
        with torch.no_grad():
            output = model(**tokens)
        sentence_vector = output.last_hidden_state.mean(dim=1).squeeze().numpy()
        return sentence_vector

    # Step 2: Image to Text
    def image_to_text(self, image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    # Step 3: Image to Vector
    def image_to_vector(self, image_path, model_name='resnet50'):
        # Use a pre-trained image embedding model like ResNet50
        # You can use torchvision.models or other deep learning frameworks
        # to load a pre-trained model and obtain the image vector.
        pass

    # Step 4: KNN Search
    def knn_search(self, query_vector, data_vectors, k=5):
        neigh = NearestNeighbors(n_neighbors=k, metric='cosine')
        neigh.fit(data_vectors)
        distances, indices = neigh.kneighbors([query_vector])
        return distances, indices

# Example usage
# Create an instance of the ImageDatabase class with a custom database name
image_db = ImageDatabase(db_name='custom_image_search.db')

dir = "images/"
for image in os.listdir(dir):
# Insert data into the database
    image_db.insert_data(image_path=dir+image, text_data=image, vector=image_db.text_to_vector('Sentence 1'))

# Retrieve data vectors from the database
data_vectors = image_db.get_data_vectors()

# Continue with the rest of the example (text_to_vector, image_to_text, image_to_vector, knn_search)
