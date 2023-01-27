from re import search
from typing import List, Union
from uuid import UUID
from sqlalchemy.orm import Session
from src.config import setup_logger
from src.files.utils import format_bucket_name
from src.pagination import OrderDirection

from src.exceptions import BaseConflictException

from src.models import Bucket, FileObject
from src.users.crud.users import UserCRUD


class FileCRUD:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.logger = setup_logger()
        self.user_crud = UserCRUD(db)

    def get_owner_bucket(self, owner_id: UUID) -> Union[Bucket, None]:
        return (
            self.db.query(Bucket)
            .filter(Bucket.name == format_bucket_name(owner_id))
            .first()
        )

    def create_bucket(self, owner_id: UUID) -> Bucket:
        if self.get_owner_bucket(owner_id):
            raise BaseConflictException("This user already has a bucket.")

        bucket_name = format_bucket_name(owner_id)
        db_bucket = Bucket(owner_id=owner_id, name=bucket_name)
        self.db.add(db_bucket)
        self.db.commit()
        self.db.refresh(db_bucket)

        return db_bucket

    def save_file(
        self,
        file_name: str,
        original_file_name: str,
        owner_id: UUID,
        total_bytes: int = 0,
    ) -> FileObject:

        db_bucket = self.get_owner_bucket(owner_id)
        if not db_bucket:
            self.logger.info(f"Creating bucket for user {owner_id}")
            db_bucket = self.create_bucket(owner_id)

        db_file_object = FileObject(
            original_file_name=original_file_name.lower(),
            file_name=file_name,
            bucket_id=db_bucket.id,
            total_bytes=total_bytes,
        )

        self.db.add(db_file_object)
        self.db.commit()
        self.db.refresh(db_file_object)

        return db_file_object

    def get_file(self, file_id: UUID) -> Union[None, FileObject]:
        db_file_object = (
            self.db.query(FileObject).filter(FileObject.id == file_id).first()
        )
        if db_file_object:
            return db_file_object

    def get_files(
        self,
        skip: int = 0,
        limit: int = 10,
        original_file_name: str = None,  # type: ignore
        owner_id: UUID = None,  # type: ignore
        order_direction: OrderDirection = OrderDirection.DESC,
    ) -> List[FileObject]:

        order_by_option = FileObject.date_created.desc()
        if order_direction == OrderDirection.ASC:
            order_by_option = FileObject.date_created.asc()

        search_filter = self.db.query(FileObject).order_by(order_by_option)

        if original_file_name is not None:
            search_filter = search_filter.filter(
                FileObject.original_file_name.contains(original_file_name.lower())
            )

        if owner_id is not None:
            search_filter = search_filter.join(Bucket).filter(
                Bucket.owner_id == owner_id
            )

        search_filter = search_filter.offset(skip).limit(limit)

        return search_filter.all()

    def remove_file(self, file_id: UUID) -> int:
        return (
            self.db.query(FileObject)
            .filter(FileObject.id == file_id)
            .delete(synchronize_session=False)
        )

    def remove_files(self, file_ids: List[UUID]) -> int:
        return (
            self.db.query(FileObject)
            .filter(FileObject.id.in_(file_ids))
            .delete(synchronize_session=False)
        )
