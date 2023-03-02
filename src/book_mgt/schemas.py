"""Pydantic Models"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, EmailStr
from src.schemas import ParentPydanticModel
from .models import Book

class Book_Base(ParentPydanticModel):
    id: UUID
    title: str
    author_id: UUID

class Book_Out(Book_Base):
    category: str
    description: str
    book_file_id: Optional[UUID]
    book_avatar_id: Optional[UUID]
    uploaded_date: Optional[datetime]
    updated_date: Optional[datetime]

class Book_info_out(ParentPydanticModel):
    title: str
    category: str
    description: str

class Book_create(ParentPydanticModel):
    title: str
    category: Optional[str]
    description: str = None
    book_file_id: Optional[UUID]
    book_avatar_id: Optional[UUID]

class Book_update(ParentPydanticModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    book_file_id: Optional[UUID] = None
    book_avatar_id: Optional[UUID] = None
    updated_date: datetime = datetime.utcnow()

class Books_out(ParentPydanticModel):
    total: int = 0
    data: list[Book_Out]

class read_book(ParentPydanticModel):
    book_id: UUID

class read_books(ParentPydanticModel):
    total: int = 0
    data: list[read_book]

class read_by(ParentPydanticModel):
    user_id: UUID

class readers(ParentPydanticModel):
    total: int = 0
    data: list[read_by]