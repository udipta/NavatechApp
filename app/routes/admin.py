from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import UserCreate
from services import authenticate_user, create_access_token, get_db

router = APIRouter(prefix="/admin")


@router.post("/login")
def admin_login(login_data: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate an organization admin and generate an access token.

    Args:
        login_data (UserCreate): The login credentials (email and password).
        db (Session): The database session, provided by the get_db dependency.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: 401 error if the email or password is incorrect.
    """

    # Define the exception to be raised for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise credentials_exception

    # Generate an access token for the authenticated admin
    access_token = create_access_token(data={"sub": user.email})

    # Return the access token and token type
    return {"access_token": access_token, "token_type": "bearer"}