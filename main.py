import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    FastAPI
                    )   

from fastapi.middleware.cors import CORSMiddleware
from routes import users,emails,AI

app = FastAPI()

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