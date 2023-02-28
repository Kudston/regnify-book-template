from src.exceptions import (
    GeneralException,
)

class Book_already_exist_exception(GeneralException):
    pass

class Book_service_not_allowed_by_user(GeneralException):
    pass

