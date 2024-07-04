import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    APIRouter,Form
                    )   

from routes import (
    session
)

from models.robot import Robot



# Create a router for API endpoints
router = APIRouter()


@router.post("/")
async def get_robots_near_to_point_based_on_radius(lalitude:float=Form(...),longitude:float=Form(...),radius:float=Form(...)):
    robots = Robot.get_robots_near_point(session,lalitude,longitude,radius)
    return [
        {
            "id": robot.id,
            "robotname": robot.robotname,
            "date": robot.date,
            "time": robot.time,
            "lalitude": robot.lalitude,
            "longitude": robot.longitude,
            "power": robot.power,
            "plastique_percentage": robot.plastique_percentage,
            "trash_percentage": robot.trash_percentage,
            "cardboard_percentage": robot.cardboard_percentage
        } for robot in robots
    ]
      
    
