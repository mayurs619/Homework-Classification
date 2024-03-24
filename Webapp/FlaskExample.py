import numpy as np
from flask import Flask, render_template, request, jsonify
from skimage import io, color, transform
import os
import cv2
import pickle

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the uploaded file is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        prediction = predict_image(full_path)
        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Invalid file format. Please upload an image (png, jpg, jpeg, gif)'})

def predict_image(image_path):
    loaded_knn = pickle.load(open('knn_classifier.pkl', 'rb'))
    pic = np.array([preprocess_image(image_path)])
    y_pred = loaded_knn.predict(pic)
    return str(y_pred[0])

def preprocess_image(image_path, target_size=(32, 32)):
    image = io.imread(image_path)
    image = color.rgb2gray(image)  # Convert to grayscale
    return cv2.resize(image, target_size).flatten()

if __name__ == '__main__':
    app.run(debug=True)
