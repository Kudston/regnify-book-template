import pytest
from src.exceptions import GeneralException
from src.book_mgt.crud import Book_crud
from src.book_mgt import schemas as book_schemas
from src.users.models  import User
from src.users.crud.users import UserCRUD
from src.book_mgt import models
from .conftest import test_book1,test_book2, test_admin_user,test_db
from src.config import setup_logger

logger = setup_logger()

def test_create_book(test_user:User, book_crud:Book_crud):
    title_under_test = "crud book create title"
    book = book_crud.create_book(author_id=test_user.id, 
                                 book_info= book_schemas.Book_create(title=title_under_test,
                                                                                              description = "descrip"))
    assert isinstance(book, models.Book)

    assert book.title==title_under_test
    assert book.author_id==test_user.id

def test_create_existing_book(test_user:User, book_crud:Book_crud):
    title_under_test = "crud book create title"
    with pytest.raises(GeneralException):
        book_crud.create_book(author_id=test_user.id, 
                              book_info= book_schemas.Book_create(title=title_under_test, 
                                                                  description = "descrip")
                                                                  )
    
def test_update_book(book_crud:Book_crud):
    title_under_test = "crud book create title"
    
    #try none existing book
    none_book = book_crud.get_book_by_title("non_existing")
    assert none_book==None

    book:models.Book = book_crud.get_book_by_title(title_under_test)
    assert book!=None

    book_crud.update_book(book.id,
                         book_schemas.Book_update(description="updated book category"))

    updated_book:models.Book = book_crud.get_book_by_title(title_under_test)
    assert updated_book.id == book.id
    assert updated_book.description=="updated book category"
    assert updated_book.title==book.title

def test_delete_book(book_crud:Book_crud):
    title_under_test = "crud book create title"
    
    book_by_title:models.Book = book_crud.get_book_by_title(title_under_test)
    book:models.Book = book_crud.get_book_by_id(book_by_title.id)
    assert book!=None

    book_crud.delete_book(book.id)
    with pytest.raises(Exception):
        deleted_book = book_crud.get_book_by_id(book.id)
        

def test_mark_read_book(test_db, book_crud:Book_crud,test_book1:models.Book, test_book2:models.Book, test_admin_user:User):
    book_id = test_book1.id
    user_id = test_admin_user.id
    user_crud = UserCRUD(test_db)
    req_user = user_crud.get_user(user_id)

    created:models.Book_read = book_crud.mark_read(req_user, book_id)

    assert created.book_id == book_id
    assert created.user_id == user_id
    read_book2:models.Book_read = book_crud.mark_read(req_user, test_book2.id)    

    read_books = book_crud.get_read_books_by_user(user_id)
    read_books_count = book_crud.get_read_book_counts((user_id))

    assert isinstance(read_books[0], models.Book_read)
    assert isinstance(read_books, list)
    assert read_books_count==2


def test_get_books_by_category(book_crud:Book_crud,test_book1:models.Book):

    books = book_crud.get_books_by_category(test_book1.category)
    
    assert isinstance(books[0], models.Book)
    assert books[0].category == test_book1.category
