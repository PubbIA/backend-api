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
    EMAIL_PROJECT,PASSWORD_EMAIL_PROJECT
)





# Create a router for API endpoints
router = APIRouter()


@router.post("/send-verification-code")
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
    
