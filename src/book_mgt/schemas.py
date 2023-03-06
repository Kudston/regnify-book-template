"""Pydantic Models"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, EmailStr
from src.schemas import ParentPydanticModel
from .models import Book
from src.users import schemas as user_schemas

class Book_Base(ParentPydanticModel):
    id: UUID
    title: str
    author_id: UUID
    
class Book_Out(Book_Base):
    category: UUID
    description: Optional[str]
    book_file_id: Optional[UUID]
    book_avatar_id: Optional[UUID]
    uploaded_date: Optional[datetime]
    updated_date: Optional[datetime]

class Book_info_out(ParentPydanticModel):
    id:UUID
    title: str
    category: Optional[UUID]
    description: Optional[str]

class Book_create(ParentPydanticModel):
    title: str
    category: Optional[UUID]
    description: Optional[str] = None
    book_file_id: Optional[UUID]
    book_avatar_id: Optional[UUID]

class Book_update(ParentPydanticModel):
    title: Optional[str] = None
    category: Optional[UUID] = None
    description: Optional[str] = None
    book_file_id: Optional[UUID] = None
    book_avatar_id: Optional[UUID] = None
    updated_date: datetime = datetime.utcnow()

class Books_out(ParentPydanticModel):
    total: int = 0
    data: list[Book_Out]

class Read_book(ParentPydanticModel):
    book: Book_info_out
    user: user_schemas.UserOut

class Read_books(ParentPydanticModel):
    total: int = 0
    data: list[Read_book] = []

class Read_by(ParentPydanticModel):
    user_id: UUID

class Readers(ParentPydanticModel):
    total: int = 0
    data: list[Read_by]