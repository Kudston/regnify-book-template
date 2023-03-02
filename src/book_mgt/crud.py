#books crud
import datetime
from typing import Union
from sqlalchemy.orm import Session
from . import models 
from src.database import setup_logger
from src.exceptions import GeneralException
from src.users.models import User
from sqlalchemy.exc import IntegrityError
from .schemas import (
    Book_Base,
    Book_create,
    Book_Out,
    Book_update,
    Book_info_out,
    Books_out,
    UUID
)

class Book_crud:
    def __init__(self,db:Session) -> None:
        self.db = db
        self.logger = setup_logger()

    def get_book_by_id(self, book_id) -> Union[models.Book, None]:
        return self.db.query(models.Book).filter(models.Book.id==book_id).first()
    
    def get_book_by_title(self, book_title):
        return self.db.query(models.Book).filter(models.Book.title==book_title).first()
    
    def get_books(self, skip =0, limit =100) -> list[models.Book]:
        return self.db.query(models.Book).offset(skip).limit(limit).all()

    def get_total_books(self) -> int:
        return self.db.query(models.Book).count()

    def get_books_for_user(self, user_id, skip =0, limit =100) -> list[models.Book]:
        return self.db.query(models.Book).filter(models.Book.author_id==user_id).offset(skip).limit(limit).all()

    def get_total_books_for_user(self, user_id:UUID) ->int:
        return self.db.query(models.Book).filter(models.Book.author_id==user_id).count()

    def create_book(self, author_id,
                     book_info:Book_create
                    ):
        try:
            book_info = book_info.dict()
            db_book = models.Book(author_id=author_id, **book_info)
            self.db.add(db_book)
            self.db.commit()
            self.db.refresh(db_book)
            return db_book
        except IntegrityError as raised_exception:
            self.logger.exception(raised_exception)
            self.logger.error(raised_exception)
            raise GeneralException("A book with that title already exist.")
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            self.logger.error(raised_exception)
            raise GeneralException(raised_exception)
        finally:
            self.db.rollback()
        

    def update_book(self, book_id, new_info:Book_update):
        
        db_book:models.Book = self.get_book_by_id(book_id)
        if not db_book:
            return GeneralException("book not found")

        new_info:dict = new_info.dict(exclude_unset=True)

        for key,value in new_info.items():
            setattr(db_book, key, value)

        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book


    def delete_book(self, book_id:UUID) -> int:
        
        db_book = self.db.query(models.Book).filter(models.Book.id==book_id)
        deleted = db_book.delete(synchronize_session=False)
        self.db.commit()
        return deleted

    def mark_read(self, user_id:UUID, book_id:UUID):
        try:
            book_read = models.read_book(book_id=book_id,user_id=user_id)
            self.db.add(book_read)
            self.db.commit()
            self.db.refresh(book_read)
            return book_read
        except IntegrityError as raised_exception:
            self.logger.exception(raised_exception)
            self.logger.error(raised_exception)
            raise GeneralException("the book is already marked as read")
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            self.logger.error(raised_exception)
            raise GeneralException(raised_exception)
        finally:
            self.db.rollback()
    
    #get books read by a user
    def get_read_books_by_user(self, user_id:UUID, skip:int =0, limit:int =100) -> list[models.read_book]:
        return self.db.query(models.read_book).filter(models.read_book.user_id==user_id).offset(skip).limit(limit).all()
    
    def get_read_book_counts(self, user_id:UUID, skip:int =0, limit:int =100) -> int:
        return self.db.query(models.read_book).filter(models.read_book.user_id==user_id).offset(skip).limit(limit).count()
    
    #get users who read a book
    def get_book_read_by(self, book_id:UUID) -> list[models.read_book]:
        return self.db.query(models.read_book).filter(models.read_book.book_id==book_id).offset(skip).limit(limit).all()
    
    def get_number_of_readers(self, book_id:UUID, skip:int =0, limit:int =100) -> int:
        return self.db.query(models.read_book).filter(models.read_book.book_id==book_id).offset(skip).limit(limit).count()
    