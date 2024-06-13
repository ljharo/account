# from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI

from .shcemas import UserShema, LoginShema, LogoutShema
from .models import UserModel, TokenModel
from .settings  import session

app = FastAPI()

@app.post('/create/user')
async def create_user(request: UserShema) -> None:
    """
    Creates a new user account.

    Args:
        request (UserShema): User data to create a new account.

    Returns:
        JSONResponse: A JSON response with a token if the user is created successfully, or an error message if the username or email already exists.

    Raises:
        400 Bad Request: If the username or email already exists.
    """
    user = UserModel()
    token = TokenModel()

    username: str = request.username
    first_name: str = request.first_name
    last_name: str = request.last_name
    email: str = request.email
    user.set_password(request.password)

    # Check if the username already exists
    username_exists: bool = session.query(session.query(UserModel).filter_by(username=username).exists()).scalar()

    if username_exists:
        error_response: dict = {
            'error': 'username',
            'sg': f'A user with the username {username} already exists.'
        }
        return JSONResponse(status_code=400, content=error_response)

    # Check if the email already exists
    email_exists: bool = session.query(session.query(UserModel).filter_by(email=email).exists()).scalar()

    if email_exists:
        error_response: dict = {
            'error': 'email',
            'sg': f'A user with the email {email} already exists.'
        }
        return JSONResponse(status_code=400, content=error_response)

    # Create the user account
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(request.password)

    session.add(user)
    session.flush()
    user_id = user.id_user

    # Create a token for the user
    token.create_token(user_id, username)
    token.id_user = user_id
    session.add(token)

    session.commit()

    # Return the token
    response: dict = {
        'token': token.token
    }
    
    return JSONResponse(status_code=200, content=response)


@app.post('/login')
async def login(request: LoginShema) -> None:
    """
    Handles user login.

    Args:
        request (LoginShema): User credentials to login.

    Returns:
        JSONResponse: A JSON response with a token if the login is successful, or an error message if the username or password is incorrect.

    Raises:
        400 Bad Request: If the username or password is incorrect.
    """
    username: str = request.username
    password: str = request.password

    # Check if the user exists
    user_query = session.query(UserModel).filter_by(username=username)
    user_exists = session.query(user_query.exists()).scalar()

    if user_exists:
        user = user_query.first()

        # Check if the password is correct
        password_is_correct = user.check_password(password)

        # Check if the user has permission to access the system
        if not user.status:
            error_response: dict = {
                'error': 'tatus',
                'sg': 'You do not have permission to access the system.'
            }
            return JSONResponse(status_code=400, content=error_response)

        if not password_is_correct:
            error_response: dict = {
                'error': 'password',
                'sg': 'Incorrect password.'
            }
            return JSONResponse(status_code=400, content=error_response)

    else:
        error_response: dict = {
            'error': 'username',
            'sg': 'The username does not exist or is misspelled.'
        }
        return JSONResponse(status_code=400, content=error_response)

    # Check if a token exists for the user
    token_exists = session.query(session.query(TokenModel).filter_by(id_user=user.id_user).exists()).scalar()

    if token_exists:
        token_query = session.query(TokenModel).filter_by(id_user=user.id_user)
        token = token_query.first()
        token_expired = token.verify_token()

        if token.uses >= 1 and token_expired:
            token.uses -= 1
            session.commit()
            return JSONResponse(status_code=200, content={'token': token.token, 'uses': token.uses})

        else:
            token.create_token(user.id_user, user.username)
            token.uses = 50
            session.commit()
            return JSONResponse(status_code=200, content={'token': token.token, 'uses': token.uses})

    else:
        token = TokenModel()
        token.create_token(user.id_user, user.username)
        token.id_user = user.id_user
        session.add(token)
        session.commit()
        return JSONResponse(status_code=200, content={'token': token.token, 'uses': token.uses})


@app.post('/logout')
async def logout(request: LogoutShema) -> None:
    """
    Handles user logout.

    Args:
        request (LogoutShema): User token and ID to logout.

    Returns:
        JSONResponse: A JSON response indicating whether the logout was successful or not.

    Raises:
        200 OK: If the logout is successful or if the token or user ID is incorrect.
    """
    user_id: int = request.id_user
    token: str = request.token

    # Check if the token exists for the user
    token_exists = session.query(session.query(TokenModel).filter_by(id_user=user_id, token=token).exists()).scalar()

    if token_exists:
        # Delete the token from the database
        token = session.query(TokenModel).filter_by(id_user=user_id, token=token).first()
        session.delete(token)
        session.commit()

        # Return a success message
        return JSONResponse(status_code=200, content={"detail": "Logout successful"})

    else:
        # Return an error message if the token or user ID is incorrect
        return JSONResponse(status_code=400, content={"error": ['id_user', 'token'], 'msg': 'The token or user ID is incorrect'})