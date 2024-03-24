import numpy as np
from flask import Flask, render_template, request, jsonify
from skimage import io, color
import os
import cv2
import pickle
import base64

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt


import tensorflow as tf
from tensorflow.keras import layers, models
import keras


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
loaded_cnn = keras.models.load_model('cnn_classifier_128.keras')

# Function to check if the uploaded file is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('file')  # Get list of files

    predictions = []
    image_data_list = []

    for file in files:
        if file.filename == '':
            continue

        if allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            pred = predict_image(full_path)
            prediction = "Homework" if (pred < 0.5) else "Not Homework"
            image_data = encode_image(full_path)
            predictions.append(prediction)
            image_data_list.append(image_data)
        else:
            return jsonify({'error': 'Invalid file format. Please upload images (jpg, jpeg).'}) 

    return jsonify({'predictions': predictions, 'image_data_list': image_data_list})

def predict_image(image_path):
    pic = np.array([preprocess_image(image_path)])
    y_pred = loaded_cnn.predict(pic)
    return y_pred[0][0]

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_image

def preprocess_image(image_path, target_size=(128, 128)):
    image = io.imread(image_path)
    image = color.rgb2gray(image)  # Convert to grayscale
    return cv2.resize(image, target_size)

if __name__ == '__main__':
    app.run(debug=True)
