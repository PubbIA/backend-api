import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, APIRouter,HTTPException
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

from typing import Union


# Create a router for API endpoints
router = APIRouter()


@router.post("/")
async def create_robot_(robotname: str = Form(...),password:str = Form(...),lalitude:float=Form(0),longitude:float=Form(0)):

    is_created = Robot.create_robot(
        session=session,robotname=robotname,
        password=password,lalitude=lalitude,
        longitude=longitude
    )

    return {"created":is_created}


@router.put("/update-position")
async def create_robot_(robotname: str = Form(...),new_lalitude:float=Form(...),new_longitude:float=Form(...)):

    robot:Robot|None=Robot.get_robot_by_robotname(session,robotname)
    if robot is None:
        raise HTTPException(status_code=401, detail=f"Invalid robotname {robotname} token")
    robot.lalitude = new_lalitude
    robot.longitude = new_longitude
    session.commit()
    
    # Update the robot in the database    
    return {"message": "Location changed successfully"}


@router.get("/")
def get_user_by_robotname_(
    robotname: str= Form(...)
    ):
    robot:Robot|None=Robot.get_robot_by_robotname(session,robotname)
    if robot is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    return {"lalitude":robot.lalitude,"longitude":robot.longitude,"robotname":robot.robotname}


@app.put("/update-info")
async def update_robot_info(
    robotname: str = Form(...),
    power: Union[int, None] = Form(None),
    plastique_percentage: Union[int, None] = Form(None),
    trash_percentage: Union[int, None] = Form(None),
    cardboard_percentage: Union[int, None] = Form(None)
):
    # Get the robot by robotname
    robot: Robot | None = Robot.get_robot_by_robotname(session, robotname)
    if robot is None:
        raise HTTPException(status_code=401, detail=f"Invalid robotname {robotname}")

    # Update the robot's power and percentages
    success = robot.update_robot(
        session=session,
        power=power,
        plastique_percentage=plastique_percentage,
        trash_percentage=trash_percentage,
        cardboard_percentage=cardboard_percentage
    )
    
    if success:
        return {"message": "Robot updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update robot")