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
class User(Base):
    """
    User model representing a user in the database.

    Attributes:
        id (str): Unique identifier for the user.
        username (str): User's username.
        email (str): User's email address (unique).
        password_hash (str): Hashed password for user authentication.
        phone_number (str): User's phone number.
        date (str): Date of the operation.
        time (str): Time of the operation.
        points (int): User's points.
        profile_image (str): url avatar image.
    """


    __table_args__ = {'extend_existing': True}

    __tablename__ = 'users'
    id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(55))
    email = Column(String(55),unique=True)
    password_hash = Column(String(255))
    phone_number = Column(String(255))
    points = Column(Numeric(2), default=0)
    date = Column(String(55), default=str(datetime.date.today()))
    time = Column(String(55), default=str(datetime.datetime.now().time()))
    profile_image = Column(String(400),default="")
    lalitude = Column(Numeric(7),default=0)
    longitude = Column(Numeric(7),default=0)
    # Define the relationship to the Operations table
    def set_password(self, password:str)->None:
        """
        Set the password for the user.

        Parameters:
            password (str): The password to set.
        """
        # Hashing the password
        self.password_hash = sha256_crypt.hash(password)

    def check_password(self, password:str)->None:
        """
        Check if the provided password matches the user's hashed password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # Verifying the password
        return sha256_crypt.verify(password, self.password_hash)

    def get_email_password(self, encryption_key:str)->str:
        """
        Decrypt and retrieve the email password for the user.

        Parameters:
            encryption_key (str): The encryption key to use for decryption.

        Returns:
            str: The decrypted email password.
        """
        # Decrypt the email password
        cipher_suite = Fernet(encryption_key)
        decrypted_password = cipher_suite.decrypt(self.email_password.encode()).decode()
        return decrypted_password

    @classmethod
    def create_user(cls, session, username:str, email:str, password:str, phone_number:str,profile_image:str,id_:str,lalitude:float,longitude:float, encryption_key:str)->bool:
        user = session.query(cls).filter(cls.email == email).first()
        if user:
            return False
        # Create a new user instance
        new_user = cls(
            id=id_ if id_ else str(uuid.uuid4()),
            username=username,
            email=email,
            phone_number=phone_number,
            profile_image=profile_image if profile_image else "",
            lalitude = lalitude if lalitude else 0,
            longitude = longitude if longitude else 0
        )
        # Set password and email password
        new_user.set_password(password)

        # Add the user to the database
        session.add(new_user)
        session.commit()
        return True

    @classmethod
    def verify_login(cls, session, email:str, password:str)->tuple[bool,Union[str,None]]:
        """
        Verify user login credentials.

        Parameters:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            tuple: A tuple containing a boolean indicating whether the login is successful and the user ID.
        """
        # Find user email
        user = session.query(cls).filter(cls.email == email).first()
        if user:
            # Verify password
            if user.check_password(password):
                # Decrypt and return email password
                user_id = user.id
                return True, user_id
        return False, None
    @classmethod
    def get_user_by_id(cls, session, user_id:str)-> Union['User', None]:
        """
        Get a user by user_id.

        Parameters:
            user_id (str): The user's ID.

        Returns:
            Union['User', None]: The user object if found, otherwise None.
        """
        return session.query(cls).filter(cls.id == user_id).first()
    @classmethod
    def get_user_by_email(cls, session, user_email:str)-> Union['User', None]:
        """
        Get a user by user_email.

        Parameters:
            user_email (str): The user's Email.

        Returns:
            Union['User', None]: The user object if found, otherwise None.
        """
        return session.query(cls).filter(cls.email == user_email).first()
    @classmethod
    def email_exists(cls, session, email: str) -> bool:
        """
        Check if an email already exists in the database.

        Parameters:
            session: SQLAlchemy session object.
            email (str): Email address to check.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        return session.query(cls).filter(cls.email == email).count() > 0

    
