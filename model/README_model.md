# Pet Emotion Detector – Model Documentation

## Overview
This CNN model classifies pet facial expressions into four emotions:
- Happy
- Sad
- Curious
- Relaxed
- Neutral

The model was trained using TensorFlow on a dataset of pet images organized by emotion labels. It outputs a predicted emotion for each image.

---

## Input Format
- RGB image, size: 224x224 pixels
- Format: JPG or PNG

---

## Output
- Predicted emotion label (one of: happy, sad, curious, relaxed, neutral)

---

## Files
- `model.h5` – Trained model file
- `labels.json` – Mapping of output indexes to emotion names

---

## How to Use the Model

### 1. Load the model:
```python
from tensorflow.keras.models import load_model
import json

model = load_model("model/model.h5")
with open("model/labels.json") as f:
    class_names = json.load(f)
```


### 2. Preprocess an image:
```python
from tensorflow.keras.preprocessing import image
import numpy as np

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array
```


### 3. Make a prediction:
```python
img = preprocess_image("dog.jpg")
prediction = model.predict(img)
predicted_label = class_names[np.argmax(prediction)]
print("Predicted Emotion:", predicted_label)
```