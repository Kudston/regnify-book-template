import pytest
from fastapi.testclient import TestClient
from src.book_mgt.crud import Book_crud
from src.book_mgt import schemas as book_schema
from src.book_mgt.service import Book_Service
from src.config import Settings
from tests.conftest import test_db
from tests.users.services.conftest import test_user,test_admin_user
from src.users.models import User


TEST_CACHE = {}

@pytest.fixture()
def book_crud(test_db):
    return Book_crud(db=test_db)

@pytest.fixture()
def test_book1(test_db, test_user:User ,book_crud: Book_crud):
    id = test_user.id
    if "test_book1" in TEST_CACHE:
        return TEST_CACHE["test_book1"]
    test_book1 = book_crud.create_book(id,
                                      book_schema.Book_create(title="test_service_title1",
                                                              description="test_book_desc"))
    TEST_CACHE['test_book1'] = test_book1
    return test_book1

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

