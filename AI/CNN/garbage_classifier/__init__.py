import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
import tensorflow as tf
import cv2
import numpy as np


PATH_TO_MODEL = "AI/CNN/garbage_classifier/garbage_classifier.h5"



# Load the model
model = tf.keras.models.load_model(PATH_TO_MODEL)


CLASSES = {"cardboard":0,"glass":2,"metal":3,"paper":1,"plastic":5,"trash":4}
SIZE = 224

def predict(path_to_image):
    img = cv2.imread(path_to_image)
    if img is not None:
        img = cv2.resize(img, 224)  # Resize images to 224x224
    # Assuming X_train[0] is the first image in your training data
    image_to_predict = np.expand_dims(img, axis=0)  # Add batch dimension if necessary

    # Make predictions
    predictions = model.predict(image_to_predict)
    predicted_class = np.argmax(predictions[0])
    classes = {value:key for key,value in CLASSES.items()}
    return classes[predicted_class]