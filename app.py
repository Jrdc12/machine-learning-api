from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from PIL import Image
import io

app = Flask(__name__)

model = load_model('my_model.h5')

# Define the classes
classes = ['bed', 'chair', 'sofa']

@app.route('/', methods=['GET'])
def index():
    return 'Hello, world!'

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image file from the request
    file = request.files['image']
    print("Uploaded file:", file.filename)

    # Create the uploads directory if it doesn't exist
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # Save the file to a temporary location
    file_path = os.path.join(uploads_dir, file.filename)
    file.save(file_path)

    with open(file_path, 'rb') as f:
        img = Image.open(io.BytesIO(f.read()))
        img.load()

    # Resize the image to 150x150 pixels
    img = img.resize((150, 150))

    # Convert the image to a numpy array
    img_array = np.array(img)

    # Normalize the pixel values (in the range of 0-1)
    img_array = img_array / 255.

    # Add a new dimension to the array to match the input shape of the model
    img_array = np.expand_dims(img_array, axis=0)

    # Make the prediction
    prediction = model.predict(img_array)

    # Get the class with highest probability
    predicted_class = classes[np.argmax(prediction)]

    # Delete the temporary file
    os.remove(file_path)

    # Return the predicted class as a JSON response
    response = {'class': predicted_class}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
