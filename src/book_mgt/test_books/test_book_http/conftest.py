import pytest
from fastapi.testclient import TestClient
from src.book_mgt.crud import Book_crud
from src.book_mgt import schemas as book_schema
from src.users.models import User
from tests.conftest import test_db
from tests.users.http.conftest import client
from src.config import Settings
from src.users.services.users import UserCRUD
from src.users import schemas as user_schemas

TEST_CACHE = {}

@pytest.fixture()
def book_crud(test_db):
    return Book_crud(db=test_db)

BOOK_SUPER_ADMIN_EMAIL = "bookadmin@regnify.com"
BOOK_SUPER_ADMIN_PASSWORD = "bookpassword"

@pytest.fixture()
def test_book_super_admin_user(
    client: TestClient, test_db
) -> dict:
    if "test_super_admin_email" in TEST_CACHE:
        return TEST_CACHE["test_super_admin_email"]

    user_crud = UserCRUD(db=test_db)
    user_created = user_crud.create_user(
        user_schemas.UserCreate(
            email=BOOK_SUPER_ADMIN_EMAIL,  # type: ignore
            first_name="Simple",
            last_name="User",
            password=BOOK_SUPER_ADMIN_PASSWORD,
        ),
        should_make_active=True,
        is_super_admin=True,
    )
    assert user_created.email == BOOK_SUPER_ADMIN_EMAIL
    assert user_created.is_active
    assert user_created.is_super_admin
    assert user_created.profile.last_name == "User"
    assert user_created.profile.first_name == "Simple"

    TEST_CACHE["test_super_admin_email"] = user_created.__dict__

    return user_created.__dict__

@pytest.fixture()
def test_book_super_admin_header(
    client:TestClient, test_db,
    response_code:int =200
) -> dict:
    if 'test_super_admin_header' in TEST_CACHE:
        return TEST_CACHE['test_super_admin_header']
    
    response = client.post('/token',
                           data= {'username':BOOK_SUPER_ADMIN_EMAIL, 'password':BOOK_SUPER_ADMIN_PASSWORD}
                           )
    assert response.status_code == response_code, response.json()
    if response.status_code==200:
        bToken = response.json()["access_token"]
        return {"Authorization": f"Bearer {bToken}"}
    
    return None

