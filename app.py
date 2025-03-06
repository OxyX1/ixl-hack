from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import pyautogui  # Import pyautogui

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('screenshare')
def handle_screenshare(data):
    # Decode the image
    img_data = base64.b64decode(data.split(',')[1])
    img = Image.open(BytesIO(img_data))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # Save the image temporarily
    cv2.imwrite('screenshot.png', img)
    
    # Process the image with pyautogui
    detected_boxes = []
    locations = pyautogui.locateAllOnScreen('target_image.png', confidence=0.8)
    for loc in locations:
        detected_boxes.append({"x": loc.left, "y": loc.top, "width": loc.width, "height": loc.height})
    
    # Emit the detected boxes to the client
    emit('detection', detected_boxes)

if __name__ == '__main__':
    socketio.run(app, debug=True)
