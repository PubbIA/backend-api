import os
import sys
import uuid
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    FastAPI, File, UploadFile, Form, status, HTTPException,APIRouter
                    )   
from exceptions.exceptions import (
                            FileExtensionException,FileNotFoundException,
                            PasswordException,EmailException,EmailConnectionFailedException,
                            LinkException,UserExistException
                            )
from emails.main import (
                            send_email_smtp,check_gmail_connection
                            )
from utils.validity import (is_gmail_password_structure,is_valid_email,
                            is_valid_password)
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
# from models import Operations,User
from models.user import User
from utils.jwt import (
                        create_access_token,decode_access_token
                      )

from utils.generate import generate_random_code
from dotenv import load_dotenv
from database import init_db
from fastapi.middleware.cors import CORSMiddleware

session=init_db()

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))
load_dotenv(dotenv_path=str(Path("./env/communication.env")))
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
FERNET_KEY:str=os.getenv("FERNET_KEY")
EMAIL_PROJECT:str=os.getenv("EMAIL_PROJECT")
PASSWORD_EMAIL_PROJECT:str=os.getenv("PASSWORD_EMAIL_PROJECT")
PDF_ENCRYPTION_SECRET:str=os.getenv("PDF_ENCRYPTION_SECRET")

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create a router for API endpoints
api_router = APIRouter(prefix="/api")

@api_router.get("/")
async def index():
    """
    Index endpoint to check if the server is running.
    """
    return {"messgae":"I am working good !"}



@api_router.post("/email/send-verification-code")
async def send_verification_email_code(to: str = Form(...),language:str = Form("fr"),length:int=Form(4),type_:str=Form("number")):
    """
    Send a verification code to the provided email address.
    """
    if not is_valid_email(to):
        raise EmailException(detail="The email form is incorrect")
    #Check the validity of email and password to connect to gmail
    if not check_gmail_connection(EMAIL_PROJECT,PASSWORD_EMAIL_PROJECT):
        raise EmailConnectionFailedException("Failed to connect to gmail.")
    code_generated:str=generate_random_code(length,type_)
    email_subject:str="Verification code"
    email_body:str=f"<h1>Your code is {code_generated}</h1>"
    is_send:bool=send_email_smtp(
        sender_email=EMAIL_PROJECT,
        sender_password=PASSWORD_EMAIL_PROJECT,
        to=to,
        email_subject=email_subject,
        email_body=email_body
    )

    return {"code":(code_generated if is_send else "")}  
    

@api_router.post("/users/email-exist")
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


@api_router.post("/users/")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone_number: str = Form(...)
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
    
        # Save user to database
        is_created:bool=User.create_user(session,username, email, password, phone_number,FERNET_KEY)
        if not is_created:
            raise UserExistException(f"User already exist with this email {email}")
        
        # Send confirmation email
        # send_email_smtp(email, "User Created", "Your account has been successfully created.")
        return {"message": "User created successfully"}
    except (EmailException, PasswordException, EmailConnectionFailedException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@api_router.post("/users/login")
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

@api_router.put("/users/change-password")
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

@api_router.get("/users")
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
    return {"username":user.username,"email":user.email,"phone_number":user.phone_number,"points":user.points}



@api_router.put("/users/points/add")
def add_points(
    points: int= Form(0),
    access_token: str= Form(...)
    ):

    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
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

@api_router.put("/users/points/deduct")
def add_points(
    points: int= Form(0),
    access_token: str= Form(...)
    ):
    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY,ALGORITHM)
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


# Include the API router in the main app
app.include_router(api_router)