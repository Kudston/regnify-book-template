import pytest
from src.service import ServiceResult
from src.users.models import User
from src.book_mgt.service import Book_Service
from src.book_mgt import models
from src.book_mgt import schemas as book_schema
from src.config import setup_logger

from .conftest import (
    book_service_test_admin,
    book_service_test_non_admin,
    test_admin_user,
    test_db,
    test_book1,
    Settings,
    )

logger = setup_logger()

def test_create_book_by_admin(book_service_test_admin:Book_Service):
    data = book_schema.Book_create(
        title="service book test",
        description= "service test description"
    )
    
    book:ServiceResult = book_service_test_admin.create_book(data)

    assert isinstance(book.data, models.Book)
    assert book.success == True
    assert book.exception == None


def test_update_book(test_admin_user:User, test_user:User, test_db):
    book_service = Book_Service(test_admin_user,
                                test_db,
                                Settings())
    
    non_owner_service = Book_Service(test_user,
                                test_db,
                                Settings())

    title_under_test = "service book test"
    data = book_schema.Book_update(
        description="updated book"
        )
    

    book = book_service.get_book_by_title(title_under_test).data

    non_user_attempt = non_owner_service.update_book(book.id, data)
    assert non_user_attempt.success == False
    assert non_user_attempt.exception != None

    book_service.update_book(book.id, data) 
    
    updated_book = book_service.get_book_by_id(book.id)

    assert isinstance(updated_book.data, models.Book)
    book_data:models.Book = updated_book.data
    assert book_data.description == "updated book"

def test_delete_book(test_admin_user:User, test_user:User, test_db):
    book_service = Book_Service(test_admin_user,
                                test_db,
                                Settings())
    
    non_owner_service = Book_Service(test_user,
                                test_db,
                                Settings())

    title_under_test = "service book test"
    
    book = book_service.get_book_by_title(title_under_test).data

    non_user_attempt = non_owner_service.delete_book(book.id)
    book_exist:ServiceResult = book_service.get_book_by_id(book.id)
    assert isinstance(book_exist.data, models.Book)
    assert non_user_attempt.success == False
    assert non_user_attempt.exception != None

    book_service.delete_book(book.id) 
    
    with pytest.raises(Exception):
        updated_book = book_service.get_book_by_id(book.id)


def test_create_marked_book(test_admin_user:User, test_db):
    book_service = Book_Service(test_admin_user,
                                test_db,
                                Settings())
    
    data = book_schema.Book_create(
        title="service mark book test",
        description= "service test description"
    )
    book:ServiceResult = book_service.create_book(data)

    assert book.data.title == "service mark book test"
    
    book_service = Book_Service(test_admin_user,
                                test_db,
                                Settings())
    mark_book:ServiceResult = book_service.mark_book_read(book.data.id)

    assert mark_book.data.user_id==test_admin_user.id
    
def test_get_books_by_category(test_admin_user:User, test_db, test_book1:models.Book):
    book_service = Book_Service(test_admin_user,
                                test_db,
                                Settings())
    result = book_service.get_books_by_category(test_book1.category)

    book_1 = result.data['data'][0]
    assert result.success == True
    assert book_1.category == test_book1.category
    assert result.data['total'] == 1  

