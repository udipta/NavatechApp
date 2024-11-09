from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .organization import Base


class User(Base):
    """
    SQLAlchemy model representing a user in the database.
    """
    __tablename__ = "users"  # Specifies the name of the database table

    # Primary key column for the user
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # User's email address, must be unique
    email = Column(String, unique=True, index=True)

    # Hashed password for the user account
    hashed_password = Column(String)

    # Foreign key referencing the organization this user belongs to
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    # Relationship to Organization
    organization = relationship("Organization", back_populates="admin")


