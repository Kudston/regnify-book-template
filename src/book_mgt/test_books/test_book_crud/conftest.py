import pytest
from src.book_mgt.crud import Book_crud
from src.book_mgt import schemas as book_schema
from src.book_mgt.service import Book_Service
from src.users.models import User
from tests.users.services.conftest import test_user,test_admin_user
from tests.conftest import test_db

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
                                      book_schema.Book_create(title="test_title1",
                                                              description="test_book_desc"))
    TEST_CACHE['test_book1'] = test_book1
    return test_book1


@pytest.fixture()
def test_book2(test_db, test_user:User ,book_crud: Book_crud):
    id = test_user.id
    test_book = book_crud.create_book(id,book_schema.Book_create(title="test_title2",
                                                              description="test_book_desc"))
    return test_book


