from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Organization, User
from app.services import SQLALCHEMY_DATABASE_URL, get_password_hash


class TestDatabase:
    def __init__(self, session: Session):
        self.session = session

    def populate_test_database(self):
        org_x = Organization(
            id=10,
            name="Test Org X",
        )

        org_y = Organization(
            id=11,
            name="Test Org Y",
        )

        org_x_admin = User(
            id=12,
            email="user@orgx.com",
            hashed_password=get_password_hash("StrongX1@password"),
            organization_id=org_x.id,
        )

        org_y_admin = User(
            id=11,
            email="user@orgy.com",
            hashed_password=get_password_hash("StrongY1@password"),
            organization_id=org_y.id,
        )

        self.session.add_all([org_x, org_y, org_x_admin, org_y_admin])
        self.session.commit()


def override_get_db():
    test_engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
