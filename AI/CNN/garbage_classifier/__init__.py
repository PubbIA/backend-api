import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Function to load the model
def load_trained_model(model_path):
    model = load_model(model_path)
    return model

# Function to preprocess a single image for prediction
def preprocess_image(image_path, target_size=(224, 224)):
    img = load_img(image_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = img_array / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    return img_array

# Function to predict the class of an image
def predict(image_path, labels):
    model_path = 'AI/CNN/garbage_classifier/garbage_classifier.h5'  # Path to your trained model
    labels_:dict={"cardboard":0,"glass":2,"metal":3,"paper":1,"plastic":5,"trash":4}

    # metal,glass => trash
    # cardboard => paper
    # plastic

    labels = {value:key for key,value in labels_.items()}  # Path to your labels file

    # Load model
    model = load_trained_model(model_path)
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    return labels[predicted_class]




if __name__=="__main__":
    model_path = 'AI/CNN/garbage_classifier/garbage_classifier.h5'  # Path to your trained model
    labels_:dict={"cardboard":0,"glass":2,"metal":3,"paper":1,"plastic":5,"trash":4}

    labels = {value:key for key,value in labels_.items()}  # Path to your labels file

    # Load model
    model = load_trained_model(model_path)
    # Example image path for prediction
    image_path = 'AI/CNN/garbage_classifier/plastique.jpeg'

    # Predict class
    predicted_label = predict_class(model, image_path, labels)
    print(f'Predicted Class: {predicted_label}')