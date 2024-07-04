import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    FastAPI
                    )   
from fastapi.middleware.cors import CORSMiddleware
from routes import robot_logs, users,emails,AI,google_drive,cashback,robots,rank,maps

# Define API information
api_info = {
    "title": "Boundif API",
    "description": "This API serves as the backend for the Smart Trash Bin project. It provides endpoints for user management, email notifications, and AI functionalities.",
    "version": "1.0.0",
    "contact": {
        "name": "LAAMIRI Ouail",
        "email": "laamiriouail@gmail.com"
    },
    "docs_url":"/api/docs"
}

# Create FastAPI instance with title, description, and author information
app = FastAPI(**api_info)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


app.include_router(users.router,prefix="/api/users", tags=["Users"])
app.include_router(emails.router,prefix="/api/email", tags=["Email"])
app.include_router(AI.router,prefix="/api/ai", tags=["Artificial intelligence"])
app.include_router(cashback.router,prefix="/api/cashback", tags=["Cashback"])
app.include_router(google_drive.router,prefix="/api/google-drive", tags=["Google drive"])
app.include_router(robots.router,prefix="/api/robots", tags=["Robot"])
app.include_router(robot_logs.router,prefix="/api/robot-logs", tags=["Robot Logs"])
app.include_router(rank.router,prefix="/api/rank", tags=["Ranking"])
app.include_router(maps.router,prefix="/api/maps", tags=["Maps"])