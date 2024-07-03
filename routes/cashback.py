import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, HTTPException,APIRouter
                    )   


# from models import Operations,User
from models.user import User
from utils.jwt import (
                        decode_access_token
                      )

from routes import (
    session,ALGORITHM,JWT_SECRET_KEY_ROBOT,JWT_SECRET_KEY
)

from enum import Enum
# Create a router for API endpoints
router = APIRouter()


class SenderEnum(str, Enum):
    app = "app"
    robot = "robot"

@router.put("/add")
def add_points(
    points: int= Form(0),
    access_token: str= Form(...),
    sender: SenderEnum= Form(SenderEnum.robot), # app
    ):

    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    if sender.lower()=="robot":
        decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY_ROBOT,ALGORITHM)
    elif sender.lower()=="app":
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

@router.put("/deduct")
def deduct_points(
    points: int= Form(0),
    access_token: str= Form(...),
    sender: SenderEnum= Form(SenderEnum.robot), # app
    ):
    # Check if points is less than zero to raise an appropriate error
    if points < 0:
        raise HTTPException(status_code=403, detail="Points cannot be negative")
    # Get the user from the database
    if sender.lower()=="robot":
        decode_token:dict=decode_access_token(access_token,JWT_SECRET_KEY_ROBOT,ALGORITHM)
    elif sender.lower()=="app":
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

