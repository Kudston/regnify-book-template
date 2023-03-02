from fastapi import APIRouter,Depends,Path
from fastapi import Security

from .crud import Book_crud
from . import schemas as book_schema
from .dependencies import initiate_Book_service
from .service import Book_Service

from src.users.models import User
from src.users.dependencies import get_current_active_user
from src.pagination import CommonQueryParams
from src.service import (
    handle_result,
)

router = APIRouter(prefix="/books", tags=["Book services"])

@router.post("/create-book", response_model=book_schema.Book_Out)
async def create_book(book_info:book_schema.Book_create, 
                book_service:Book_Service = Security(initiate_Book_service)
                ):
    #call the book crud to create book
    result = book_service.create_book(book_info)
    
    #send mail with information on newly created book

    #return result
    return handle_result(result=result, expected_schema= book_schema.Book_Out)

@router.get("/my-books",
            response_model=book_schema.Books_out)
def get_books_for_user(common:CommonQueryParams = Depends(),
            book_service:Book_Service = Security(initiate_Book_service)
    ):
    result = book_service.get_user_books(common.skip, common.limit)
    
    return result.data#handle_result(result, book_schema.Books_out)


@router.get("/",
            response_model=book_schema.Books_out)
def get_books(common: CommonQueryParams = Depends(),
            book_service:Book_Service = Security(initiate_Book_service)
    ):
    result = book_service.get_books(common.skip,common.limit)
    return result.data #handle_result(result, book_schema.Books_out)

@router.get("/read-book/{book_title}",
            response_model=book_schema.Book_Out)
def get_book_by_title(book_title: str, 
            book_service:Book_Service = Security(initiate_Book_service)
            ):
    result = book_service.get_book_by_title(book_title=book_title)
    return handle_result(result, book_schema.Book_Out)

@router.get("/{book_id}", 
            response_model=book_schema.Book_Out)
def get_book_by_id(book_id:book_schema.UUID, 
            book_service:Book_Service = Security(initiate_Book_service)
            ):
    result = book_service.get_book_by_id(book_id)
    return handle_result(result, book_schema.Book_Out)

@router.put("/{book_id}", 
            response_model= book_schema.Book_Out)
def update_book(book_id:book_schema.UUID ,
            new_info:book_schema.Book_update,
            book_service:Book_Service = Security(initiate_Book_service)
    ):

    result = book_service.update_book(book_id,new_info)

    return handle_result(result, book_schema.Book_Out)

@router.delete("/{book_id}/delete")
def delete_book(book_id:book_schema.UUID,
            book_service:Book_Service = Security(initiate_Book_service)
    ):
    result = book_service.delete_book(book_id)
    return handle_result(result)


@router.post('/mark-book/{book_id}',
             response_model=book_schema.read_book)
async def mark_book(book_id:book_schema.UUID, 
                book_service:Book_Service = Security(initiate_Book_service)
                ):
    #call the book crud to mark book
    result = book_service.mark_book_read(book_id)
    
    #send mail with information on newly created book

    #return result
    return handle_result(result=result, expected_schema= book_schema.read_book)
