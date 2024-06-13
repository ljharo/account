from pydantic import BaseModel

class UserShema(BaseModel):
    """
    User schema for creating a new user.

    Represents the data required to create a new user account.
    """

    # Username chosen by the user
    username: str
    
    # User's first name
    first_name: str
    
    # User's last name
    last_name: str
    
    # User's email address
    email: str
    
    # User's password (hashed for security)
    password: str


class LoginShema(BaseModel):
    """
    Login schema for user authentication.

    Represents the data required to authenticate a user.
    """

    # Username to authenticate
    username: str
    
    # Password to authenticate (hashed for security)
    password: str


class LogoutShema(BaseModel):
    """
    Logout schema for revoking a user's token.

    Represents the data required to revoke a user's token.
    """

    # ID of the user to revoke the token for
    id_user: int
    
    # Token to revoke
    token: str