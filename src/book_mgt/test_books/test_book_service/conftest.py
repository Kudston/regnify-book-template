import pytest
from fastapi.testclient import TestClient
from src.book_mgt.crud import Book_crud
from src.book_mgt import schemas as book_schema
from src.book_mgt.service import Book_Service
from src.config import Settings
from tests.conftest import test_db
from tests.users.services.conftest import test_user,test_admin_user



TEST_CACHE = {}

@pytest.fixture()
def book_service_test_admin(test_db, test_admin_user):

    if "book_service" in TEST_CACHE:
        return TEST_CACHE["book_service"]
    book_service =  Book_Service(test_admin_user, 
        test_db, Settings())
    
    TEST_CACHE["book_service"] = book_service
    return book_service


@pytest.fixture()
def book_service_test_non_admin(test_db, test_user):

    if "book_service2" in TEST_CACHE:
        return TEST_CACHE["book_service2"]
    book_service =  Book_Service(test_user, 
        test_db, Settings())
    
    TEST_CACHE["book_service2"] = book_service
    return book_service

