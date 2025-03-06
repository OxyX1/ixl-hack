from flask import Flask, render_template, request, jsonify
import pyautogui
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filepath': filepath})
    return jsonify({'error': 'File upload failed'})

@app.route('/trace', methods=['POST'])
def trace_image():
    data = request.get_json()
    filepath = data.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'})

    # Load the image using OpenCV
    image = cv2.imread(filepath)
    if image is None:
        return jsonify({'error': 'Failed to load image'})

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect edges in the image
    edges = cv2.Canny(gray, 50, 150)

    # Find contours in the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours using pyautogui
    for contour in contours:
        for point in contour:
            x, y = point[0]
            pyautogui.moveTo(x, y)
            pyautogui.click()

    return jsonify({'message': 'Image traced successfully'})

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
