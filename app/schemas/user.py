import re

from pydantic import BaseModel, EmailStr, field_validator

from services import validate_password


class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.
    """

    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        """
        Validate the password.
        """
        return validate_password(v)


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # Allows the model to work with ORM (Object-Relational Mapping) objects
