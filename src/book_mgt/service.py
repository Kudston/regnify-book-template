from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from typing import Union


from src.users import schemas as user_schema
from src.service import (
    BaseService,
    ServiceResult,
    failed_service_result,
    success_service_result,
    )
from src.config import Settings, setup_logger
from src.exceptions import (
    BaseForbiddenException,
    GeneralException,
    BaseNotFoundException,
)

from .crud import Book_crud
from .models import Book
from . import schemas as book_schema
from .exceptions import (
    Book_already_exist_exception,
    Book_service_not_allowed_by_user,
)

class Book_Service(BaseService):
    def __init__(
        self, requesting_user: user_schema.UserOut, db: Session, app_settings: Settings
    ) -> None:
        super().__init__(requesting_user, db)
        self.book_crud = Book_crud(db)
        self.app_settings: Settings = app_settings
        self.logger = setup_logger()
        

        if requesting_user is None:
            raise GeneralException("Requesting User was not provided.")
    
    def create_book(
        self, book: book_schema.Book_create
    ) -> ServiceResult[Union[Book, None]]:
        db_book: Book = self.book_crud.get_book_by_title(book_title= book.title)
        
        if db_book:
            return ServiceResult(
                data=None,
                success= False,
                exception= GeneralException(f'book already exist')
            )
        try:            
            if not  self.requesting_user.is_active:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception= Book_service_not_allowed_by_user("user not allowed to create book")
                )
            user_id = self.requesting_user.id
            created_book = self.book_crud.create_book(user_id, book_info=book)
        except GeneralException as raised_exception:
            return failed_service_result(raised_exception)
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
        return ServiceResult(data=created_book, success=True)

    def update_book(
        self, book_id:UUID,
        new_book_info:book_schema.Book_update
    ) -> ServiceResult[Union[Book, None]]:
        try:
            db_book:Book = self.book_crud.get_book_by_id(book_id)

            if not db_book:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception="Book does not exist"
                )
            if  (not self.requesting_user.is_super_admin) or (not db_book.author_id==self.requesting_user.id):
                return ServiceResult(
                    data=None,
                    success=False,
                    exception="not allowed to perform operation"
                )
            
            updated = self.book_crud.update_book(book_id,new_book_info)
                        
            return ServiceResult(
                data = updated,
                success= True
                )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)

    def delete_book(
        self, book_id:UUID  
        ) -> ServiceResult[Union[Book]]:
        try:
            db_book:Book = self.book_crud.get_book_by_id(book_id)

            if not db_book:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception="Book does not exist"
                )
            if  db_book.author_id!=self.requesting_user.id:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception="not allowed to perform operation"
                )
            deleted_book = self.book_crud.delete_book(book_id)

            return ServiceResult(
                data=deleted_book,
                success=True
            )
        except Exception as raised_exception:
            return failed_service_result(raised_exception)


    def get_book_by_title(
        self, book_title: str
    ) -> ServiceResult[Union[Book, None]]:
        try:
            db_book: Book = self.book_crud.get_book_by_title(book_title=book_title)

            if db_book is None:
                return ServiceResult(
                    data=None,
                    success= False,
                    exception= GeneralException(f'book does not exist')
                )
            

            return ServiceResult(
                data=db_book,
                success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
    
    def get_book_by_id(
        self, book_id:UUID
    ) -> ServiceResult[Union[Book, None]]:
        try:
            db_book:Book = self.book_crud.get_book_by_id(book_id=book_id)
            
            if db_book is None:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception=GeneralException(f'book does not exist')
                )
            return ServiceResult(
            data=db_book,
            success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
        
    
    def get_user_books(
        self, skip:int =0, limit:int =100
    ) -> ServiceResult:
        try:
            if not self.requesting_user.is_super_admin:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception=f'user is not active'   
                )
            
            user_id = self.requesting_user.id
            
            db_books = self.book_crud.get_books_for_user(user_id=user_id, skip=skip, limit=limit)
            
            books_count = self.book_crud.get_total_books_for_user(user_id=user_id)
            
            book_data = {"total":books_count, "data":db_books}
            
            
            return ServiceResult(
                data=book_data,
                success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
    
    def get_books(self, 
                  skip:int =0, limit:int =100
    ) -> ServiceResult:
        if not self.requesting_user.is_super_admin:
            return ServiceResult(
                data=None,
                success=False,
                exception = f'you are not allowed to perform this action'
            )
        try:
            db_books = self.book_crud.get_books(skip, limit)
            book_count = self.book_crud.get_total_books()
            data = {"total":book_count, "data":db_books}
            return ServiceResult(
                data=data,
                success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)

    #marking books as read
    def mark_book_read(self,
                       book_id:UUID) -> ServiceResult:
        

        try:
            db_book:Book = self.book_crud.get_book_by_id(book_id)

            if not db_book:
                return ServiceResult(
                    data=None,
                    success=False,
                    exception="Book does not exist"
                )
            
            mark_read = self.book_crud.mark_read(self.requesting_user.id, book_id)
        except GeneralException as raised_exception:
            return failed_service_result(raised_exception)
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
        return ServiceResult(data=mark_read, success=True)

    def get_read_book_by_user(self, skip: int =0, limit: int =100) -> ServiceResult:
        try:
            books_read = self.book_crud.get_read_books_by_user(self.requesting_user.id, skip,limit)
            total_books = self.book_crud.get_read_book_counts(self.requesting_user.id, skip, limit)

            data = {'total':total_books, 'data':books_read}
            
            return ServiceResult(
                data=data,
                success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)

    def get_read_by(self,book_id:UUID, skip: int =0, limit: int =100) -> ServiceResult:
        try:
            books_read = self.book_crud.get_book_read_by(book_id, skip,limit)
            total_books = self.book_crud.get_number_of_readers(book_id, skip, limit)

            data = {'total':total_books, 'data':books_read}
            
            return ServiceResult(
                data=data,
                success=True
            )
        except Exception as raised_exception:
            self.logger.exception(raised_exception)
            return failed_service_result(raised_exception)
