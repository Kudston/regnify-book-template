import pytest
from datetime import timedelta
from jose import jwt
from src.exceptions import GeneralException
from src.security import create_access_token, get_password_hash
from src.users.crud import UserCRUD
from src.users.models import Profile, User
from src.users.schemas import UserCreate, UserOut, UserUpdate

from src.config import setup_logger

logger = setup_logger()


def test_create_access_token(app_settings):
    data = {
        "sub": "1@regnify.com",
        "is_active": True,
        "is_super_admin": False,
        "roles": [],
    }
    access_token_expires = timedelta(minutes=app_settings.access_code_expiring_minutes)
    token = create_access_token(
        data,
        expires_delta=access_token_expires,
        secret_key=app_settings.secret_key,
        algorithm=app_settings.algorithm,
    )

    payload = jwt.decode(
        token=token,
        key=app_settings.secret_key,
        algorithms=[app_settings.algorithm],
    )

    assert "sub" in payload
    assert payload["sub"] == "1@regnify.com"
    assert "is_active" in payload
    assert payload["is_active"]
    assert "is_super_admin" in payload
    assert not payload["is_super_admin"]
    assert "roles" in payload
    assert payload["roles"] == []


def test_create_user(test_db):
    email_under_test = "3@regnify.com"
    users_crud: UserCRUD = UserCRUD(db=test_db)
    user: User = users_crud.create_user(
        UserCreate(email=email_under_test, last_name="1", first_name="2", password="3")
    )
    logger.info(user.email)
    assert user.email == email_under_test


def test_create_user_with_existing_email(user_crud: UserCRUD):
    email_under_test = "3@regnify.com"

    with pytest.raises(GeneralException):
        user_crud.create_user(
            UserCreate(
                email=email_under_test, last_name="1", first_name="2", password="3"
            )
        )


def test_update_user(user_crud: UserCRUD):
    email_under_test = "3@regnify.com"

    # * getting user with a wrong email address
    none_user = user_crud.get_user_by_email("no-user@regnify.com")
    assert none_user == None

    user = user_crud.get_user_by_email(email_under_test)
    assert user != None

    user_crud.update_user(
        user.id, UserUpdate(first_name="User3", last_name="3User", is_active=False, is_super_admin=False)  # type: ignore
    )

    updated_user: User = user_crud.get_user(user.id)  # type: ignore

    assert updated_user.email == email_under_test
    assert isinstance(updated_user.profile, Profile)
    assert updated_user.profile.last_name == "3User"
    assert updated_user.profile.first_name == "User3"
    assert not updated_user.is_active
    assert not updated_user.is_super_admin


def test_change_password(user_crud: UserCRUD):
    email_under_test = "3@regnify.com"
    old_user = user_crud.get_user_by_email(email_under_test)
    assert old_user != None
    old_hashed_password = old_user.hashed_password
    hashed_password = get_password_hash("new-password")
    new_user = user_crud.update_user_password(old_user.id, hashed_password)  # type: ignore
    assert new_user.hashed_password != old_hashed_password
