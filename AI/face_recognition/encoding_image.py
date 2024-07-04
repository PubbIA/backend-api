import sys
import os
# Add parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

import csv
import face_recognition
import cv2
from pathlib import Path

import numpy as np

def get_image_encoding(image_path: Path) -> list:
    """
    Get face encoding from an image.

    Args:
        image_path (Path): Path to the image file.

    Returns:
        np.ndarray | None: The encoding of the specified image if found, None otherwise.

    Raises:
        None

    Examples:
        >>> image_path = Path("ouail.jpg")
        >>> encoding = get_image_encoding(image_path)
        >>> if encoding is not None:
        >>>     print("Face encoding:", encoding)
    """
    if not image_path.exists():
        print("Error: Image file does not exist.")
        return None
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            print("Error: Could not read the image file.")
            return None
        encoding = face_recognition.face_encodings(image)[0]
        return encoding
    except IndexError:
        print("No face detected in the image.")
        return None

def get_image_encoding_from_csv(image_name: str, csv_filename: Path) -> list :
    """
    Get image encoding from a CSV file for a specific image.

    Args:
        image_name (str): Name of the image.
        csv_filename (Path): Path to the CSV file containing image encodings.

    Returns:
        np.ndarray | None: The encoding of the specified image if found, None otherwise.
    """
    # Read the CSV file
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == image_name:
                # Convert the string representation of encoding to a list of floats
                encoding = np.array([float(value) for value in row[1].replace('[','').replace(']','').split()])
                return encoding
    return None

def get_images_encoding_from_csv(csv_filename: Path) -> list :
    """
    Get image encoding from a CSV file for a specific image.

    Args:
        image_name (str): Name of the image.
        csv_filename (Path): Path to the CSV file containing image encodings.

    Returns:
        np.ndarray | None: The encoding of the specified image if found, None otherwise.
    """
    # Read the CSV file
    data = []
    with open(csv_filename, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            data.append(
                {
                    "id":row[0],
                    "encoding":row[1]
                }
            )
    return data


def extract_encodings(image_folder:Path) -> dict:
    """
    Extract face encodings from images in a folder.

    Args:
        image_folder (str): Path to the folder containing images.

    Returns:
        dict: A dictionary containing image names as keys and their encodings as values.
    """
    encodings_dict = {}
    for image_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_name)
        face_encodings = get_image_encoding(Path(image_path))
        if face_encodings is not None:
            if len(face_encodings) > 0:
                encodings_dict[image_name] = face_encodings
            else:
                print(f"No face detected in {image_name}")
    return encodings_dict

def write_encodings_to_csv(encodings_dict:dict, csv_filename:Path):
    """
    Write encodings dictionary to a CSV file.

    Args:
        encodings_dict (dict): Dictionary containing image names as keys and their encodings as values.
        csv_filename (str): Name of the CSV file to be created.
    """
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image Name', 'encodings'])
        for image_name, embedding in encodings_dict.items():
            writer.writerow([image_name, embedding])

def add_encoding_to_csv(image_name: str, encoding: np.ndarray, csv_filename: Path) -> bool:
    """
    Add a new encoding to an existing CSV file or update an existing encoding.

    Args:
        image_name (str): Name of the image.
        encoding (np.ndarray): The encoding to be added or updated.
        csv_filename (Path): Path to the CSV file containing image encodings.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """

    try:
        updated = False
        rows = []

        if csv_filename.exists():
            with open(csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                for row in reader:
                    if row[0] == image_name:
                        row[1] = encoding
                        updated = True
                    rows.append(row)
        else:
            header = ['Image Name', 'Encoding']

        if not updated:
            rows.append([image_name, encoding])

        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"Encoding added/updated in {csv_filename}")
        return True

    except Exception as e:
        print(f"Error adding/updating encoding to CSV: {e}")
        return False

if __name__=="__main__":
    # Usage
    image_folder = "images"
    csv_filename = "encodings.csv"

    # Extract encodings from images in the folder
    # encodings_dict = extract_encodings(image_folder)

    # Write encodings to a CSV file
    # write_encodings_to_csv(encodings_dict, csv_filename)

    # print(f"encodings saved to {csv_filename}")

    # Read encodings from the CSV file
    encodings=extract_encodings(Path("images"))
    print( encodings )
