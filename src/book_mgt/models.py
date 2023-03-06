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
    author_id = Column(ForeignKey('users.id')) #consider foreignkey with user
    author =   relationship('User', foreign_keys=[author_id], lazy='joined')
    title  = Column(String, unique=True)
    description = Column(String)
    category    = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4)
    book_file_id = Column(postgresql.UUID(as_uuid=True),
        nullable=True
        )
    book_avatar_id = Column(postgresql.UUID(as_uuid=True),
        nullable=True)
    uploaded_date = Column(DateTime, default=datetime.datetime.utcnow)
    updated_date  = Column(DateTime, nullable=True)

class Book_read(Base):
    __tablename__ = "Books_read"

    book_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('Book.id'), primary_key=True)
    book    = relationship('Book', foreign_keys=[book_id],lazy='joined')

    user_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    user    = relationship('User', foreign_keys=[user_id], lazy='joined')

    read_date = Column(DateTime, default=datetime.datetime.utcnow)
    