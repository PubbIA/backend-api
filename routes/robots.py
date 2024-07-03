import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, APIRouter
                    )   
from exceptions.exceptions import (
                            EmailException,EmailConnectionFailedException,
                            )
from emails.main import (
                            send_email_smtp,check_gmail_connection
                            )
from utils.validity import (is_valid_email)
from utils.generate import generate_random_code
from routes import (
    session,FERNET_KEY
)
from models.robot import Robot




# Create a router for API endpoints
router = APIRouter()


@router.post("/")
async def create_robot_(robotname: str = Form(...),password:str = Form(...),location:str=Form(...)):

    is_created = Robot.create_robot(
        session=session,robotname=robotname,
        password=password,location=location,
        encryption_key=FERNET_KEY
    )

    return {"created":is_created}
    
