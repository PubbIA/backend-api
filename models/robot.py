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
    robotname = Column(String(55),unique=True)
    password_hash = Column(String(255))
    date = Column(String(55), default=str(datetime.date.today()))
    time = Column(String(55), default=str(datetime.datetime.now().time()))
    lalitude = Column(Numeric(7),default=0)
    longitude = Column(Numeric(7),default=0)
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
    def create_robot(cls, session: Session, robotname: str, password: str, lalitude: float, longitude: float) -> bool:
        # Check if a robot with the given name already exists
        # Set a default robotname if not provided
        if not robotname:
            base_name = "boundif"
            count = session.query(cls).filter(cls.robotname.like(f"{base_name}%")).count()
            robotname = f"{base_name}-{count + 1}"
        existing_robot = session.query(cls).filter_by(robotname=robotname).first()
        if existing_robot:
            print(f"Robot with name {robotname} already exists.")
            return False

        # Create a new robot instance
        new_robot = cls(
            robotname=robotname,
            lalitude=lalitude if lalitude else 0,
            longitude=longitude if longitude else 0,
        )
        # Set password and email password
        new_robot.set_password(password)

        # Add the robot to the database
        session.add(new_robot)
        session.commit()
        return True

    @classmethod
    def get_robot_by_robotname(cls, session, robotname:str)-> Union['Robot', None]:
        """
        Get a user by user_id.

        Parameters:
            user_id (str): The user's ID.

        Returns:
            Union['User', None]: The user object if found, otherwise None.
        """
        return session.query(cls).filter(cls.robotname == robotname).first()

    
    def update_robot(self, session: Session, power: Union[int, None] = None, plastique_percentage: Union[int, None] = None,
                     trash_percentage: Union[int, None] = None, cardboard_percentage: Union[int, None] = None) -> bool:
        """
        Update the robot's power and percentages if the provided values are not None.

        Parameters:
            power (Union[int, None]): The new power value.
            plastique_percentage (Union[int, None]): The new plastique percentage value.
            trash_percentage (Union[int, None]): The new trash percentage value.
            cardboard_percentage (Union[int, None]): The new cardboard percentage value.

        Returns:
            bool: True if the robot was updated, False otherwise.
        """
        if power is not None:
            self.power = power
        if plastique_percentage is not None:
            self.plastique_percentage = plastique_percentage
        if trash_percentage is not None:
            self.trash_percentage = trash_percentage
        if cardboard_percentage is not None:
            self.cardboard_percentage = cardboard_percentage

        session.commit()
        return True



