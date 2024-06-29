import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from fastapi import (
                    File, UploadFile, HTTPException,APIRouter
                    )   

import shutil
from pathlib import Path

from AI.CNN import garbage_classifier

from utils import create_folder


# Create a router for API endpoints
router = APIRouter()



@router.post("/garbage-classifier")
async def save_image(image: UploadFile = File(...)):
    # Check if the temporary folder exists, create it if not
    create_folder("temp")
    create_folder("data")

    # Check if the uploaded file has a valid image extension
    allowed_extensions = ('.jpg', '.jpeg', '.png')
    file_extension = Path(image.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid image format. Supported formats: jpg, jpeg, png")

    # Save the uploaded image
    with open(f"temp/{image.filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Perform image processing or any other operations here
    # For example, you can call your computer vision functions here
    predicted_class:bool=garbage_classifier.predict(Path(f"temp/{image.filename}"))
    # Remove the temporary image file
    os.remove(f"temp/{image.filename}")

    return {"class": predicted_class}

