from sqlalchemy import Column, Integer, String, event, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy.orm.attributes import backref_listeners

Base = declarative_base()


class Organization(Base):
    """
    SQLAlchemy model representing an organization in the database.
    """
    __tablename__ = "organizations"  # Specifies the name of the database table

    # Primary key column for the organization
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Name of the organization, must be unique
    name = Column(String, unique=True, index=True)

    # Dynamic DB URL of the organization, must be unique and not null
    db_url = Column(String, index=True, nullable=True)

    # Relationship to User
    admin = relationship('User', back_populates='organization', uselist=False)
