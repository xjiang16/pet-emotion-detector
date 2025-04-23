import os
import tensorflow as tf
from tensorflow.keras import layers, models
import json

# Paths to image folders
train_dir = "data/train"
val_dir = "data/val"

img_height = 224
img_width = 224
batch_size = 32
epochs = 10
subset_size = 2048

tmp_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size
)
class_names = tmp_ds.class_names
print(f"🧾 Detected classes: {class_names}")


# Load limited train/val
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    shuffle=True,
    seed=42
).take(subset_size // batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    val_dir,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    shuffle=True,
    seed=42
).take(512 // batch_size)


# Normalize images
normalization_layer = layers.Rescaling(1./255)
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=AUTOTUNE)

# Define the CNN model
model = models.Sequential([
    layers.Input(shape=(img_height, img_width, 3)),

    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Conv2D(128, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),  # Dropout 50%
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(train_ds, validation_data=val_ds, epochs=epochs)

# Save
os.makedirs("/tmp/model", exist_ok=True)
model.save("/tmp/model/model.keras")
with open("/tmp/model/labels.json", "w") as f:
    json.dump(class_names, f)

print("✅ Training complete. Model saved to /tmp/model/")