# models.py

import jwt
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from passlib.hash import bcrypt
from datetime import datetime, timedelta

from .settings import SECRET_KEY, Base, engine


class RolModel(Base):
    """
    Role model for the database.

    Represents a role entity in the database, with attributes such as
    role ID, name, and description.
    """

    __tablename__ = 'roles'  # Table name in the database.

    # Unique identifier for the role
    id_rol = Column(Integer, primary_key=True)
    
    # Unique name for the role (e.g. "Admin", "User", etc.)
    name = Column(String(length=50), unique=True)
    
    # Brief description of the role
    description = Column(String(length=255))


class UserModel(Base):
    """
    User model for the database.

    Represents a user entity in the database, with attributes such as
    username, password, email, etc.
    """

    __tablename__ = 'users'  # Table name in the database.

    id_user = Column(Integer, primary_key=True)  # Unique user identifier.
    id_rol = Column(Integer, ForeignKey('roles.id_rol'))  # Role identifier associated with the user.
    username = Column(String(length=50), unique=True)  # Unique username.
    firts_name = Column(String(length=50))  # First name of the user.
    last_name = Column(String(length=50))  # Last name of the user.
    email = Column(String(length=255), unique=True)  # Unique email address for the user.
    password = Column(String(length=255))  # User password (stored securely).
    date_create = Column(DateTime, default=func.now())  # Date the user was created.
    status = Column(Boolean(), default=True)  # User status (active/inactive).

    def set_password(self, password: str) -> None:
        """
        Sets the user's password.

        Hashes the password using bcrypt and stores it in the database.

        Args:
            password: The password to set.
        """
        self.password = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the stored one.

        Uses bcrypt to verify the password.

        Args:
            password: The password to verify.

        Returns:
            True if the password matches, False otherwise.
        """
        return bcrypt.verify(password, self.password)


class TokenModel(Base):
    """
    Token model for the database.

    Represents a token entity in the database, with attributes such as
    user ID, token value, number of uses, and creation date.
    """

    __tablename__: str = 'tokens'  # Table name in the database.

    id_user = Column(Integer, ForeignKey('users.id_user'))  # Foreign key referencing the user ID.
    token = Column(String(length=255), unique=True, primary_key=True)  # Unique token value.
    uses = Column(Integer, default=50)  # Number of times the token can be used.
    date_create = Column(DateTime, default=func.now())  # Date the token was created.

    def create_token(self, id_user: int, username: str) -> str:
        """
        Creates a new token for the given user.

        Generates a payload with the user's information, encodes it using JWT,
        and stores the resulting token in the database.

        Args:
            id_user: The ID of the user to create the token for.
            username: The username of the user to create the token for.

        Returns:
            The generated token as a string.
        """
        # Create a payload with the user's information
        payload = {
            'user_id': id_user,
            'username': username,
            'exp': datetime.now() + timedelta(days=5)  # Token is valid for 5 days
        }
        
        # Generate the token
        self.token: str = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    def verify_token(self) -> bool:
        """
        Verifies the validity of the token.

        Decodes the token using JWT and checks if it's valid.

        Returns:
            True if the token is valid, False otherwise.
        """
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=['HS256'])
            return True
        
        except jwt.ExpiredSignatureError:
            return False  # Token has expired
        
        except jwt.InvalidTokenError:
            return False  # Token is not valid


Base.metadata.create_all(engine)