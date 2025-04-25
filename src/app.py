from flask import Flask, request, render_template
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import json

app = Flask(__name__, template_folder="../templates", static_folder="../static")

MODEL_PATH = "../model/model.h5"
LABELS_PATH = "../model/labels.json"

model = load_model(MODEL_PATH)

with open(LABELS_PATH) as f:
    class_names = json.load(f)

# Preprocessing function
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    
    # Save file to uploads folder
    save_path = os.path.join('../uploads', file.filename)
    file.save(save_path)
    
    # Preprocess and predict
    img_array = preprocess_image(save_path)
    prediction = model.predict(img_array)
    predicted_label = class_names[np.argmax(prediction)]

    return f"Predicted Emotion: {predicted_label}", 200

if __name__ == '__main__':
    os.makedirs('../uploads', exist_ok=True)
    app.run(debug=True)