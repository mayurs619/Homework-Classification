import numpy as np
from flask import Flask, render_template, request, jsonify
from skimage import io, color, transform
import os
import cv2
import pickle
import base64

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
        pred = predict_image(full_path)
        if(pred == "0.0"):
            prediction = "Homework"
        else:
            prediction = "Not Homework"
        image_data = encode_image(full_path)
        return jsonify({'prediction': prediction, 'image': image_data})
    else:
        return jsonify({'error': 'Invalid file format. Please upload an image (png, jpg, jpeg, gif)'})

def predict_image(image_path):
    loaded_knn = pickle.load(open('knn_classifier.pkl', 'rb'))
    pic = np.array([preprocess_image(image_path)])
    y_pred = loaded_knn.predict(pic)
    return str(y_pred[0])

def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_image

def preprocess_image(image_path, target_size=(32, 32)):
    image = io.imread(image_path)
    image = color.rgb2gray(image)  # Convert to grayscale
    return cv2.resize(image, target_size).flatten()

if __name__ == '__main__':
    app.run(debug=True)
