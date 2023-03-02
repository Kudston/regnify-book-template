"""Contains the DB modules"""
import uuid
import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from src.database import Base
from src.users.models import User

class Book(Base):
    __tablename__ = "Book"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    author_id = Column(postgresql.UUID(as_uuid=True)) #consider foreignkey with user
    title  = Column(String, unique=True)
    description = Column(String)
    category    = Column(String, default="others")
    book_file_id = Column(postgresql.UUID(as_uuid=True),
        nullable=True
        )
    book_avatar_id = Column(postgresql.UUID(as_uuid=True),
        nullable=True)
    uploaded_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date  = Column(DateTime, nullable=True)

class read_book(Base):
    __tablename__ = "Books_read"

    book_id = Column(postgresql.UUID(as_uuid=True),
                primary_key=True)
    user_id = Column(postgresql.UUID(as_uuid=True),
                     primary_key=True)
    read_date = Column(DateTime, default=datetime.datetime.utcnow)
    