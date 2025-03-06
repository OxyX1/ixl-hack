from flask import Flask, send_from_directory, request
import base64
from PIL import Image
import io
import tensorflow as tf

app = Flask(__name__, static_folder='public')

# Load a pre-trained model (for example, MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    image_data = data['image'].split(',')[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('RGB')  # Convert to RGB
    
    # Preprocess the image for the model
    image = image.resize((224, 224))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    image_array = tf.expand_dims(image_array, 0)
    
    # Make a prediction
    predictions = model.predict(image_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
    observation = decoded_predictions[0][1]  # Get the class label

    return {'observation': observation}, 200

if __name__ == '__main__':
    app.run(debug=True)
