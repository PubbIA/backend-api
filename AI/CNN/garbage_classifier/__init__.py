import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Define the label dictionary
labels_ = {0: "cardboard", 1: "paper", 2: "glass", 3: "metal", 4: "trash", 5: "plastic"}

def predict(image_path: str,model_path: str='AI/CNN/garbage_classifier/garbage_classifier.h5') -> str:
    # Load the model
    model = load_model(model_path)
    
    # Load the image
    image = cv2.imread(image_path)
    
    # Preprocess the image
    image = cv2.resize(image, (224, 224))  # Resize the image to the input size of the model
    image = image / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    
    # Predict the class
    predictions = model.predict(image)
    predicted_class = np.argmax(predictions[0])
    
    # Get the class label
    class_label = labels_[predicted_class]
    
    return class_label


if __name__=="__main__":
    model_path = 'AI/CNN/garbage_classifier/garbage_classifier.h5'  # Path to your trained model
    # labels_:dict={"cardboard":0,"glass":2,"metal":3,"paper":1,"plastic":5,"trash":4}

    # labels = {value:key for key,value in labels_.items()}  # Path to your labels file

    # Load model
    # model = load_model(model_path)
    # Example image path for prediction
    image_path = 'AI/CNN/garbage_classifier/plastique.jpeg'

    # Predict class
    predicted_label = predict(model_path, image_path)
    print(f'Predicted Class: {predicted_label}')