import tensorflow as tf
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import io
import logging
from keras.layers import TFSMLayer
from keras import Input, Model

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Model path
MODEL_PATH = '/home/ubuntu/pet_emotion_model'

# Class labels
CLASS_LABELS = ['angry', 'happy', 'relaxed', 'sad']

# Load model
try:
    layer = TFSMLayer(MODEL_PATH, call_endpoint='serving_default')
    input_tensor = Input(shape=(224, 224, 3))
    output_tensor = layer(input_tensor)
    model = Model(inputs=input_tensor, outputs=output_tensor)
    logging.info("Model loaded successfully using TFSMLayer")
except Exception as e:
    logging.error(f"Error loading model via TFSMLayer: {e}")
    raise

# Preprocess image
def preprocess_image(image):
    try:
        image = image.resize((224, 224))
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        return image_array
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        raise

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Pet Emotion Detector</title>
            <style>
                body { font-family: Arial; padding: 40px; text-align: center; }
                input[type="file"] { margin: 20px; }
                button { padding: 10px 20px; font-size: 16px; }
            </style>
        </head>
        <body>
            <h2>Upload an Image of Your Pet</h2>
            <form method="POST" action="/predict" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*" required><br>
                <button type="submit">Detect Emotion</button>
            </form>
        </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        image = Image.open(image_file).convert('RGB')

        image_array = preprocess_image(image)
        logging.info(f"Image shape after preprocessing: {image_array.shape}")

        predictions = model.predict(image_array)
        logging.info(f"Raw predictions: {predictions}")

        # Check output shape and convert if needed
        if predictions is None or len(predictions) == 0:
            raise ValueError("Model returned no predictions.")

        # If predictions is a dictionary, get first item
        if isinstance(predictions, dict):
            predictions = list(predictions.values())[0]

        predicted_class = CLASS_LABELS[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))

        logging.info(f"Predicted: {predicted_class}, Confidence: {confidence:.4f}")

        if request.content_type.startswith('multipart/form-data'):
            return f'''
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h2>Prediction Result</h2>
                <p><strong>Emotion:</strong> {predicted_class}</p>
                <p><strong>Confidence:</strong> {confidence:.2f}</p>
                <a href="/">Try Another</a>
            </body>
            </html>
            '''
        else:
            return jsonify({
                'emotion': predicted_class,
                'confidence': confidence
            })

    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/model-summary')
def model_summary():
    try:
        stringlist = []
        model.summary(print_fn=lambda x: stringlist.append(x))
        summary_html = "<br>".join(stringlist)
        response = f"""
        <html>
        <body>
        <h2>Pet Emotion Model Summary</h2>
        <pre style='font-family: monospace;'>{summary_html}</pre>
        </body>
        </html>
        """
        logging.info("Model summary requested")
        return response
    except Exception as e:
        logging.error(f"Error generating model summary: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
