from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import User
from models import Organization
from schemas import OrganizationCreate, OrganizationResponse
from services import get_db, create_org_database, get_password_hash

router = APIRouter(prefix="/org")


@router.post("/create", response_model=OrganizationResponse)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    """
    Create a new organization.

    Args:
        org (OrganizationCreate): The organization data to be created.
        db (Session): The database session, provided by the get_db dependency.

    Returns:
        OrganizationResponse: The newly created organization.

    Raises:
        HTTPException: 400 error if the organization already exists.
    """

    # Check if an organization with the given name already exists
    db_org = db.query(Organization).filter(Organization.name == org.name).first()
    if db_org:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already exists")

    # Check if a user with the given email already exists
    db_user = db.query(User).filter(User.email == org.admin_email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    try:
        # Create the organization first
        db_org = Organization(name=org.name)

        # Set the db_url using the method from the Pydantic model
        db_org.db_url = org.generate_db_url()

        db.add(db_org)
        db.flush()  # This will assign an id to db_org without committing the transaction

        # Create the user with a reference to the organization
        hashed_password = get_password_hash(org.admin_password)
        db_user = User(email=org.admin_email, hashed_password=hashed_password, organization_id=db_org.id)
        db.add(db_user)

        db.commit()
        db.refresh(db_org)

        # Create the organization's database
        create_org_database(org=db_org)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # Return the newly created organization
    return db_org


@router.get("/get/{organization_name}", response_model=OrganizationResponse)
def get_organization(organization_name: str, db: Session = Depends(get_db)):
    """
    Retrieve an organization by its name.

    Args:
        organization_name (str): The name of the organization to retrieve.
        db (Session): The database session, provided by the get_db dependency.

    Returns:
        OrganizationResponse: The organization details if found.

    Raises:
        HTTPException: 404 error if the organization is not found.
    """
    # Query the database for an organization with the given name
    db_org = db.query(Organization).filter(Organization.name == organization_name).first()

    # If no organization is found, raise a 404 Not Found error
    if not db_org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Return the found organization
    return db_org

