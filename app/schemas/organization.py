from pydantic import BaseModel, EmailStr, field_validator

from schemas.user import UserResponse
from services import validate_password


class OrganizationCreate(BaseModel):
    """
    Pydantic model for creating a new organization.
    """
    name: str
    admin_email: EmailStr
    admin_password: str

    @field_validator('admin_password')
    def validate_admin_password(cls, v):
        """
        Validate the admin password.
        """
        return validate_password(v)

    def generate_db_url(self) -> str:
        """
        Generate a dynamic DB URL based on the organization name and admin email.

        Returns:
            str: The generated database URL.
        """

        from services.database import database_url_parser
        return str(database_url_parser(self.name, self.admin_email))


class OrganizationResponse(BaseModel):
    """
    Pydantic model for the response when retrieving organization information.
    """
    id: int
    name: str
    admin: UserResponse

    class Config:
        from_attributes = True  # Allows the model to work with ORM (Object-Relational Mapping) objects
