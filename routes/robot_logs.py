import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    Form, APIRouter,HTTPException
                    )   
from models.robot_logs import RobotLog

from routes import (
    session
)



# Create a router for API endpoints
router = APIRouter()


@router.get("/all")
async def get_all_robots_logs():
    logs = RobotLog.get_all_logs(session)
    if not logs:
        return []
    return [
        {
            "id": log.id,
            "robot_id": log.robot_id,
            "operation": log.operation,
            "timestamp": log.timestamp,
            "details": log.details
        }
        for log in logs
    ]
    
@router.get("/{robot_id}")
async def get_logs_by_robot_id(robot_id:str):
    logs = RobotLog.get_logs_by_robot_id(session, robot_id)
    if not logs:
        return []
    return [
        {
            "id": log.id,
            "robot_id": log.robot_id,
            "operation": log.operation,
            "timestamp": log.timestamp,
            "details": log.details
        }
        for log in logs
    ]


