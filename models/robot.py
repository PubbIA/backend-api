import uuid
from sqlalchemy import Column, String,Numeric
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet  # For encryption
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from database import Base
import datetime


# Define User model
class Robot(Base):
    __table_args__ = {'extend_existing': True}

    __tablename__ = 'robots'
    id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    robotname = Column(String(55))
    password_hash = Column(String(255))
    date = Column(String(55), default=str(datetime.date.today()))
    time = Column(String(55), default=str(datetime.datetime.now().time()))
    location = Column(String(400),default="")
    power = Column(Numeric(3),default=0)
    plastique_percentage = Column(Numeric(3),default=0)
    trash_percentage = Column(Numeric(3),default=0)
    cardboard_percentage = Column(Numeric(3),default=0)
    
    # Define the relationship to the Operations table
    def set_password(self, password:str)->None:
        """
        Set the password for the robot.

        Parameters:
            password (str): The password to set.
        """
        # Hashing the password
        self.password_hash = sha256_crypt.hash(password)


    def check_password(self, password:str)->None:
        """
        Check if the provided password matches the robot's hashed password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # Verifying the password
        return sha256_crypt.verify(password, self.password_hash)
    
    @classmethod
    def create_robot(cls, session, username:str, password:str, id_:str,location:str, encryption_key:str)->bool:
        # Create a new robot instance
        new_robot = cls(
            id=id_ if id_ else str(uuid.uuid4()),
            robotname=username,
            location = location if location else ""
        )
        # Set password and email password
        new_robot.set_password(password)

        # Add the robot to the database
        session.add(new_robot)
        session.commit()
        return True






