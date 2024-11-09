import os
import re
import secrets
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from models import User

SECRET_KEY = os.getenv("APP_SECRET", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


def validate_password(password: str):
    """
    Validate the given password against security criteria.

    This function checks if the password meets the following requirements:
    - At least 8 characters long
    - Contains at least one lowercase letter
    - Contains at least one uppercase letter
    - Contains at least one digit
    - Contains at least one special character from !@#$%^&*(),.?":{}|<>

    Args:
        password (str): The password to validate.

    Returns:
        str: The validated password if it meets all criteria.

    Raises:
        ValueError: If the password does not meet any of the specified criteria.
    """
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')

    # Check for at least one digit
    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one digit')

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError('Password must contain at least one special character')

    return password


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches, False otherwise.
    """

    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password):
    """
    Generate a hash for the given password.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict):
    """
    Create a new JWT access token.

    Args:
        data (dict): The payload to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user based on their email and password.

    This function queries the database for a user with the given email,
    and if found, verifies the provided password against the stored hash.

    Args:
        db (Session): The database session to use for querying.
        email (str): The email address of the user trying to authenticate.
        password (str): The plain text password provided by the user.

    Returns:
        User | bool: If authentication is successful, returns the User object.
                     If authentication fails, returns False.
    """

    try:
        validate_password(password)
    except ValueError:
        return False
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


