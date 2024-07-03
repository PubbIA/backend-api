import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, status, HTTPException,APIRouter,UploadFile,File
                    )   

from fastapi.responses import JSONResponse

from exceptions.exceptions import (
                            PasswordException,EmailException,EmailConnectionFailedException,
                            UserExistException
                            )
from pathlib import Path

from google_drive.main import upload_file_to_drive
from utils import create_folder
import shutil
from utils.validity import (is_valid_email,
                            is_valid_password)
# from models import Operations,User
from models.user import User
from utils.jwt import (
                        create_access_token,decode_access_token
                      )
from AI.face_recognition.take_image import detect_person_with_face_eyes_nose_mouth
from AI.face_recognition.encoding_image import add_encoding_to_csv,get_image_encoding
from routes import (
    JWT_SECRET_KEY,FERNET_KEY,session,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES,JWT_SECRET_KEY_ROBOT
)

import uuid

# Create a router for API endpoints
router = APIRouter()

    

@router.post("/email-exist")
async def check_email_exist(email: str = Form(...)):
    """
    Check if an email exists.
    """
    if not is_valid_email(email):
        raise EmailException(detail="The email form is incorrect")
    user:User|None=User.get_user_by_email(session,email)
    if user:
        access_token = create_access_token(user.id,5,JWT_SECRET_KEY,ALGORITHM)
        return {"exist":True,"access_token":access_token}
    return {"exist":False,"access_token":""}


@router.post("/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone_number: str = Form(...),
    user_profile:UploadFile=File(None)
):
    """
    Create a new user.
    """
    try:
        
        # Check if email is valid
        if not is_valid_email(email):
            raise EmailException("Invalid email")

        # Check if email password has correct structure
        if not is_valid_password(password):
            raise PasswordException("Invalid password structure")
        is_created=False
        if user_profile:
            create_folder("temp")
            create_folder("data")
            # Create the path
            csv_filename = Path("data/encodings.csv")
            # Save the uploaded image
            with open(f"temp/{user_profile.filename}", "wb") as buffer:
                shutil.copyfileobj(user_profile.file, buffer)
            
            valid_image:bool=detect_person_with_face_eyes_nose_mouth(Path(f"temp/{user_profile.filename}"))
            if valid_image:
                id_=str(uuid.uuid4())
                result:bool=add_encoding_to_csv(id_, get_image_encoding(Path(f"temp/{user_profile.filename}")),csv_filename)

                if result:
                    # Remove the temporary image file
                    profile_image_url = upload_file_to_drive(Path(f"temp/{user_profile.filename}"),"pubai")
                    is_created:bool=User.create_user(session,username, email, password, phone_number,profile_image_url,id_,FERNET_KEY)
                    
                    os.remove(f"temp/{user_profile.filename}")
                    return {"message": "User created successfully"}
            else:
                os.remove(f"temp/{user_profile.filename}")
                return HTTPException(status_code=400,detail="The image profile not respect the requirements")
        else:
            # Save user to database
            is_created:bool=User.create_user(session,username, email, password, phone_number,None,None,FERNET_KEY)
        if not is_created:
            raise UserExistException(f"User already exist with this email {email} or you have a problem in connexion")
        
        # Send confirmation email

        return {"message": "User created successfully"}
    except (EmailException, PasswordException, EmailConnectionFailedException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """
    User login.
    """
    # Verify login credentials
    is_valid_login, user_id = User.verify_login(session,email, password)
    
    if not is_valid_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(user_id,ACCESS_TOKEN_EXPIRE_MINUTES,JWT_SECRET_KEY,ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/change-password")
def change_password(
    new_password: str= Form(...),
    access_token: str= Form(...)
    ):
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    # Check if email password has correct structure
    if not is_valid_password(new_password):
        raise PasswordException("Invalid password structure")
    # Set the new password
    user.set_password(new_password)
    session.commit()
    
    # Update the user in the database    
    return {"message": "Password changed successfully"}

@router.get("/")
def get_user_by_access_token_(
    access_token: str= Form(...)
    ):
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return {"username":user.username,"email":user.email,"phone_number":user.phone_number,"points":user.points,"profile_image":user.profile_image}



@router.put("/points/add")
def add_points(
    points: int= Form(0),
    access_token: str= Form(...)
    ):

    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY_ROBOT,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user.points+=points
    # Set the new password
    session.commit()
    
    # Update the user in the database    
    if points<10:
        return {"message": f"{points} point added to {user.username} successfully"}
    return {"message": f"{points} points added to {user.username} successfully"}

@router.put("/points/deduct")
def deduct_points(
    points: int= Form(0),
    access_token: str= Form(...)
    ):
    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY_ROBOT,ALGORITHM)
    if not decode_token["valid"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user_id:str=decode_token["user_id"]
    user:User|None=User.get_user_by_id(session,user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if user.points<points:
        raise HTTPException(status_code=401, detail="Insufficient points")
    user.points-=points
    # Set the new password
    session.commit()
    
    # Update the user in the database    
    if points<10:
        return {"message": f"{points} point deducted from {user.username} successfully"}
    return {"message": f"{points} points deducted from {user.username} successfully"}




