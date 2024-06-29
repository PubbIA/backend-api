from dotenv import load_dotenv
from database import init_db
import os
from pathlib import Path


session=init_db()
# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))
load_dotenv(dotenv_path=str(Path("./env/communication.env")))
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
FERNET_KEY:str=os.getenv("FERNET_KEY")
EMAIL_PROJECT:str=os.getenv("EMAIL_PROJECT")
PASSWORD_EMAIL_PROJECT:str=os.getenv("PASSWORD_EMAIL_PROJECT")