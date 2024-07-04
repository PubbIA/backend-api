import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    APIRouter
                    )   

from routes import (
    session
)

from models.user import User



# Create a router for API endpoints
router = APIRouter()


@router.get("/")
async def get_all_users_classed_by_its_points():
    """
    Send a verification code to the provided email address.
    """
    users = User.get_all_users_ordered_by_total_points(session)
    return [
        {"username":user.username,"email":user.email,"phone_number":user.phone_number,
            "points":user.points,"profile_image":user.profile_image,"lalitude":user.lalitude,
            "longitude":user.longitude,"points_totale":user.points_totale} for user in users
    ]
      
    
