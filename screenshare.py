import cv2
import numpy as np
import base64
import requests
from PIL import ImageGrab

def capture_screen():
    screen = np.array(ImageGrab.grab())
    _, buffer = cv2.imencode('.jpg', screen)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

def send_screenshare():
    url = 'http://localhost:5000/screenshare'
    while True:
        img_str = capture_screen()
        requests.post(url, data={'image': img_str})

if __name__ == '__main__':
    send_screenshare()
