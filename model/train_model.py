import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, TensorBoard
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check GPU availability
try:
    gpus = tf.config.list_physical_devices('GPU')
    logging.info(f"Num GPUs Available: {len(gpus)}")
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
except Exception as e:
    logging.error(f"Error checking GPU: {e}")

# Dataset path (update if different on EC2)
dataset_path = '/home/ubuntu/EE5423-final-project/data'
if not os.path.exists(dataset_path):
    logging.error(f"Dataset path {dataset_path} does not exist")
    raise FileNotFoundError(f"Dataset path {dataset_path} does not exist")

# Image dimensions and hyperparameters
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 4  # angry, happy, relaxed, sad

# Data augmentation for training
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(dataset_path, 'train'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(dataset_path, 'val'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)


# Check class distribution
logging.info(f"Class indices: {train_generator.class_indices}")
class_counts = {cls: sum(train_generator.labels == idx) for cls, idx in train_generator.class_indices.items()}
logging.info(f"Class distribution: {class_counts}")

# Compute class weights for imbalance
try:
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_generator.labels),
        y=train_generator.labels
    )
    class_weights = dict(enumerate(class_weights))
    logging.info(f"Class weights: {class_weights}")
except Exception as e:
    logging.warning(f"Error computing class weights: {e}")
    class_weights = None

# Optimize data pipeline
try:
    train_dataset = tf.data.Dataset.from_generator(
        lambda: train_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 224, 224, 3], [None, NUM_CLASSES])
    ).cache().prefetch(tf.data.AUTOTUNE)

    val_dataset = tf.data.Dataset.from_generator(
        lambda: val_generator,
        output_types=(tf.float32, tf.float32),
        output_shapes=([None, 224, 224, 3], [None, NUM_CLASSES])
    ).cache().prefetch(tf.data.AUTOTUNE)
except Exception as e:
    logging.error(f"Error creating tf.data pipeline: {e}")
    raise

# Transfer learning with MobileNetV2
try:
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze all layers initially

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(NUM_CLASSES, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
except Exception as e:
    logging.error(f"Error building model: {e}")
    raise

# Compile model
try:
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
except Exception as e:
    logging.error(f"Error compiling model: {e}")
    raise

# Callbacks
callbacks = [
    ReduceLROnPlateau(monitor='val_loss', patience=2, factor=0.5, verbose=1),
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    TensorBoard(log_dir='/tmp/logs', histogram_freq=1)  # For monitoring
]

# Train
try:
    model.fit(
        train_dataset,
        epochs=10,
        validation_data=val_dataset,
        callbacks=callbacks,
        class_weight=class_weights
    )
except Exception as e:
    logging.error(f"Error during training: {e}")
    raise

# Save model
try:
    model.save('/tmp/pet_emotion_model_mobilenetv2')  # SavedModel format
    logging.info("Model saved successfully")
except Exception as e:
    logging.error(f"Error saving model: {e}")
    raise

# Evaluate model
try:
    val_loss, val_accuracy = model.evaluate(val_dataset)
    logging.info(f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}")
except Exception as e:
    logging.error(f"Error evaluating model: {e}")