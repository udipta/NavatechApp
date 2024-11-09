import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse

from models.organization import Base, Organization

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def database_url_parser(org_name: str, org_admin_email: str):
    """
    Reconstruct base database URL with org_name, using SQLAlchemy's URL object.

    Args:
        org_name (str): The organization name.
        org_admin_email (str): The organization admin email.

    Returns:
        sqlalchemy_url (str): The new database URL.
    """

    database = org_name.replace(' ', '_').lower()

    # Parse the URL
    parsed_url = urlparse(SQLALCHEMY_DATABASE_URL)

    # Reconstruct using SQLAlchemy's URL object
    sqlalchemy_url = URL.create(
        drivername="postgresql",
        username=org_admin_email,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port,
        database=database
    )

    return sqlalchemy_url


def create_db(db_name, db_user, db_pass):
    """
    Create a new database and user for an organization.

    This function attempts to create a new database and user in PostgreSQL.
    If the user already exists, it will not create a new one.
    If the database already exists, it will not create a new one.

    Args:
        db_name (str): The name of the database to create.
        db_user (str): The username for the database owner.
        db_pass (str): The password for the database user. If None, creates user without password.

    Raises:
        Exception: Any exception that occurs during the database or user creation process.
    """
    try:
        # Create the dynamic DB for the organization and grant necessary permissions to admin user
        with engine.connect() as conn:
            # Check if the user exists
            user_exists = conn.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname = '{db_user}'")).fetchone()
            if not user_exists:
                if db_pass:
                    conn.execute(text(f'CREATE USER "{db_user}" WITH PASSWORD {db_pass};'))
                else:
                    conn.execute(text(f'CREATE USER "{db_user}"'))
            # Check if the db exists
            db_exist = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")).fetchone()
            if not db_exist:
                conn.execute(text(f'CREATE DATABASE "{db_name}" WITH OWNER "{db_user}";'))

        print(f'Database {db_name} now available with {db_user}')
    except Exception as e:
        raise e


def create_org_database(org: Organization):
    """
    Create a new database for an organization and set up its schema.

    Args:
        org (Organization): The organization details.

    Returns:
    """

    # Construct the database URL
    db_url = database_url_parser(org.name, org.admin.email)

    db_name = db_url.database
    db_user = db_url.username
    db_pass = db_url.password

    # Create the database and user
    create_db(db_name, db_user, db_pass)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
