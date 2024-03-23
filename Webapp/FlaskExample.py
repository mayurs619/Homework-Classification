import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from skimage import io, color, transform
import matplotlib.pyplot as plt
import os
import cv2
import pickle
from flask import Flask, render_template, request, redirect, url_for
import os

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
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
    else:
        return "Invalid file format. Please upload an image (png, jpg, jpeg, gif)."

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    
    loaded_knn = pickle.load(open('knn_classifier.pkl', 'rb'))
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pic = np.array([preprocess_image(full_path)])
    y_pred = loaded_knn.predict(pic)
    print(y_pred)
    return str(y_pred)
    
    #return testing()
    #return f'Image {filename} uploaded successfully.'

def testing():
    
    return "hello"

def preprocess_image(image_path, target_size=(32, 32)):
    image = io.imread(image_path)
    image = color.rgb2gray(image)  # Convert to grayscale
    return cv2.resize(image, target_size).flatten()



if __name__ == '__main__':
    app.run(debug=True)
