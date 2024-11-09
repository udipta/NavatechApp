from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database
from app.main import app
from app.services import get_db
from .fixtures import create_and_delete_database
from .utils import override_get_db, Organization


client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


def test_org_create_api_success():
    response = client.post(
        "/org/create",
        json={"name": "Test Org", "admin_email": "test@example.com", "admin_password": "Strong1@password"}
    )
    assert response.status_code == 200
    assert "id" in response.json()

    # Check Dynamic DB Test
    org_id = response.json()["id"]
    db_org = next(get_db()).query(Organization).filter(Organization.id == org_id).first()
    assert db_org.name == "Test Org"
    assert database_exists(db_org.db_url)

    # Drop DB After Test
    drop_database(db_org.db_url)


def test_org_get_api_success():
    response = client.get("/org/get/Test Org X")
    assert response.status_code == 200
    assert response.json().get("name") == "Test Org X"
    assert response.json().get("id") == 10


def test_org_create_api_failure():
    response = client.post(
        "/org/create",
        json={"org_name": "Test Org X", "admin_email": "test@example.com", "admin_password": "Strong1@password"}
    )
    assert response.status_code != 200
    assert "id" not in response.json()


def test_org_get_api_failure():
    response = client.get("/org/get/Test X")
    assert response.status_code != 200
    assert "name" not in response.json()


def test_admin_apis_success():
    response = client.post(
        "/admin/login",
        json={"email": "user@orgx.com", "password": "StrongX1@password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_admin_apis_failure():
    response = client.post(
        "/admin/login",
        json={"email": "testX@example.com", "password": "Strong1@password"}
    )
    assert response.status_code != 200
    assert "access_token" not in response.json()

