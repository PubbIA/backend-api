import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, APIRouter,UploadFile,File
                    )   
from fastapi.exceptions import HTTPException
from exceptions.exceptions import (
                            EmailException,EmailConnectionFailedException,
                            )

from pathlib import Path

from google_drive.main import upload_file_to_drive
from utils import create_folder
import shutil
from AI.face_recognition.take_image import detect_person_with_face_eyes_nose_mouth
from AI.face_recognition.encoding_image import add_encoding_to_csv,get_image_encoding
from utils.jwt import decode_access_token
from routes import (
    JWT_SECRET_KEY,session,ALGORITHM
)
from models.user import User

# Create a router for API endpoints
router = APIRouter()


@router.post("/user-profile")
def upload_user_profile(access_token: str= Form(...),user_profile:UploadFile=File(...)):
    # Check if the temporary folder exists, create it if not
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    create_folder("temp")
    create_folder("data")
    # Create the path
    csv_filename = Path("data/encodings.csv")

    # Save the uploaded image
    with open(f"temp/{user_profile.filename}", "wb") as buffer:
        shutil.copyfileobj(user_profile.file, buffer)
    
    valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{user_profile.filename}"))
    if valid_image:
        result:bool=add_encoding_to_csv(user.id, get_image_encoding(Path(f"temp/{user_profile.filename}")),csv_filename)
        if result:
            # Remove the temporary image file
            profile_image_url = upload_file_to_drive(Path(f"temp/{user_profile.filename}"),"pubai")
            user.profile_image=profile_image_url
            session.commit()
            os.remove(f"temp/{user_profile.filename}")
            return {"valid_image": valid_image}

    # Remove the temporary image file
    os.remove(f"temp/{user_profile.filename}")

    return {"valid_image": valid_image}
