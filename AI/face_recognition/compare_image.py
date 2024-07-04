import os
import sys
import numpy 

# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

import face_recognition
from pathlib import Path
import numpy as np
from AI.face_recognition.encoding_image import get_image_encoding,get_image_encoding_from_csv,get_images_encoding_from_csv


def compare_faces(known_image_path: Path, unknown_image_path: Path) -> bool:
    """
    Compare faces in two images.

    Args:
        known_image_path (Path): Path to the image file containing the known face.
        unknown_image_path (Path): Path to the image file containing the unknown face.

    Returns:
        bool | None: True if faces match, False if faces don't match, None if there's an error.

    Raises:
        None

    Examples:
        >>> known_image_path = Path("ouail.jpg")
        >>> unknown_image_path = Path("messi.jpeg")
        >>> result = compare_faces(known_image_path, unknown_image_path)
        >>> if result is not None:
        >>>     print("Face match:", result)
    """
    if not known_image_path.exists() or not unknown_image_path.exists():
        print("Error: One or both image files do not exist.")
        return None
    try:

        # Proceed with face encoding if images loaded successfully
        known_encoding = get_image_encoding(known_image_path)
        unknown_encoding = get_image_encoding(unknown_image_path)
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return True if str(results[0])== "True" else False
    except IndexError:
        print("No faces detected in one of the images.")
        return None


def compare_face_use_csv_encoding(known_image_name: str, unknown_image_path: Path, csv_filename: Path) -> bool :
    if not unknown_image_path.exists() or not csv_filename.exists():
        print("Error: Image file or CSV file does not exist.")
        return None
    try:
        known_encoding = get_image_encoding_from_csv(known_image_name, csv_filename)
        if known_encoding is None:
            return False
        unknown_encoding = get_image_encoding(unknown_image_path)
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return True if str(results[0])== "True" else False
    except IndexError:
        print("No faces detected in one of the images.")
        return False


def get_face_use_csv_encoding(unknown_image_path: Path, csv_filename: Path) -> dict:
    if not unknown_image_path.exists() or not csv_filename.exists():
        print("Error: Image file or CSV file does not exist.")
        return {"exist": False, "user_id": ""}
    
    try:
        known_encodings = get_images_encoding_from_csv(csv_filename)
        if not known_encodings:  # Check if known_encodings is empty
            return {"exist": False, "user_id": ""}
        
        unknown_encoding = get_image_encoding(unknown_image_path)
        user_id = ""
        for i in known_encodings:
            encoding_values = np.array([float(value) for value in i["encoding"].replace('[','').replace(']','').split()])
            results = face_recognition.compare_faces([encoding_values], unknown_encoding)
            if results and results[0]:
                user_id = i["id"]
                break
        
        return {"exist": bool(user_id), "user_id": user_id}
    
    except IndexError:
        print("No faces detected in one of the images.")
        return {"exist": False, "user_id": ""}





if __name__=="__main__":
    import time
    start = time.time()
    print( compare_face_use_csv_encoding("ouail.jpg",Path("images/unknown.jpg"),Path("encodings.csv")))
    end = time.time()
    print("Time:",end-start)

    start = time.time()
    print(compare_faces(Path("images/ouail.jpg"),Path("images/unknown.jpg")))
    end = time.time()
    print("Time:",end-start)
    




