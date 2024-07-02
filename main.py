import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    FastAPI
                    )   

from fastapi.middleware.cors import CORSMiddleware
from routes import users,emails,AI

# Define API information
api_info = {
    "title": "Poubbelle Intelligente API",
    "description": "This API serves as the backend for the Smart Trash Bin project. It provides endpoints for user management, email notifications, and AI functionalities.",
    "version": "1.0.0",
    "contact": {
        "name": "LAAMIRI Ouail",
        "email": "laamiriouail@gmail.com"
    }
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


app.include_router(users.router,prefix="/api/users", tags=["users"])
app.include_router(emails.router,prefix="/api/email", tags=["email"])
app.include_router(AI.router,prefix="/api/ai", tags=["ai"])