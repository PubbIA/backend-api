import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    File, UploadFile, HTTPException,APIRouter,Form
                    )   

import shutil
from pathlib import Path

from AI.CNN import garbage_classifier
from AI.chatboot import get_random_quote,get_recyclage_idea
from utils import create_folder
from AI.face_recognition.take_image import detect_person_with_face_eyes_nose_mouth
from AI.face_recognition.compare_image import compare_face_use_csv_encoding,get_face_use_csv_encoding
from utils.jwt import decode_access_token
from routes import (
    JWT_SECRET_KEY,session,ALGORITHM
)

from models.user import User

# Create a router for API endpoints
router = APIRouter()



@router.post("/garbage-classifier")
async def grabage_classifier_(image: UploadFile = File(...)):
    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    predicted_class:bool=garbage_classifier.predict(Path(f"temp/{image.filename}"))
    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"class": predicted_class}

@router.post("/face-recognition")
async def check_between_photo_and_all_user_profiles(image: UploadFile = File(...)):
    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Check if the file exists, if not, create it
    if not csv_filename.exists():
        csv_filename.touch()

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))
    if not valid_image:
        # Remove the temporary image file
        os.remove(f"temp/{image.filename}")
        return {"valid_image": valid_image,"exist":False,"user_id":""}
    # Check if the image matches the face encoding in the CSV file
    result:dict=get_face_use_csv_encoding(Path(f"temp/{image.filename}"),csv_filename)

    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"exist": result["exist"],"user_id":result["user_id"],"valid_image":True}

@router.post("/face-recognition/check")
async def check_between_photo_and_user_profile(access_token:str=Form(...),image: UploadFile = File(...)):
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Check if the file exists, if not, create it
    if not csv_filename.exists():
        csv_filename.touch()

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))
    if not valid_image:
        # Remove the temporary image file
        os.remove(f"temp/{image.filename}")
        return {"valid_image": valid_image}
    # Check if the image matches the face encoding in the CSV file
    result:bool=compare_face_use_csv_encoding(user.id,Path(f"temp/{image.filename}") ,csv_filename)

    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"valid_image": result}


@router.post("/image-of-persone")
async def check_if_a_personne_on_a_image(image: UploadFile = File(...)):
    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Check if the file exists, if not, create it
    if not csv_filename.exists():
        csv_filename.touch()

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{image.filename}"))

    return {"valid_image":valid_image}


@router.post("/chat/recyclage")
async def get_recyclage_idea_(question:str=Form(...)):
    return {"idea":get_recyclage_idea(question=question)}

@router.post("/chat/quote")
async def get_random_quote_(language:str=Form("English")):
    return {"quote":get_random_quote(language=language)}
