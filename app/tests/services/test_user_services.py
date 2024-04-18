from app.schemas.user import User, UserLogin
from app.db.models import User as UserModel
from app.repositories.sqlalchemy.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository
)
from app.services.user_services import UserServices
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import pytest
import pytz
import os


crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

brazilian_timezone = pytz.timezone('America/Sao_Paulo')


def test_register_user_service(db_session):
    user = User(username='carlos', password='pass123!',
                email='carlos@email.com', is_staff=False)

    repository = SQLAlchemyUserRepository(db_session, UserModel)

    services = UserServices(repository)

    services.register_user(user)

    user_on_db = services.repository.find_first()

    assert user_on_db is not None
    assert user_on_db.username == user.username
    assert crypt_context.verify(user.password, user_on_db.password)

    services.repository.remove(user_on_db)


def test_register_user_already_exists_username_service(db_session):
    user = User(username='carlos', password='pass123!',
                email='carlos@email.com', is_staff=False)

    user2 = User(username='carlos', password='pass12342323!',
                 email='foo@bar.com', is_staff=False)

    repository = SQLAlchemyUserRepository(db_session, UserModel)

    services = UserServices(repository)

    services.register_user(user)

    with pytest.raises(HTTPException):
        services.register_user(user2)

    user_on_db = services.repository.find_first()
    services.repository.remove(user_on_db)


def test_login_user_service(db_session, user_on_db):
    user = UserLogin(username='foo', password='pass123!')

    repository = SQLAlchemyUserRepository(db_session, UserModel)
    services = UserServices(repository)

    token_data = services.user_login(user)

    assert token_data.expires_at < datetime.now(
        brazilian_timezone) + timedelta(31)


def test_login_user_invalid_username_service(db_session, user_on_db):
    user = UserLogin(username='carlos', password='pass123!')

    repository = SQLAlchemyUserRepository(db_session, UserModel)
    services = UserServices(repository)

    with pytest.raises(HTTPException):
        services.user_login(user)


def test_login_user_invalid_password_service(db_session, user_on_db):
    user = UserLogin(username='foo', password='pass123')

    repository = SQLAlchemyUserRepository(db_session, UserModel)
    services = UserServices(repository)

    with pytest.raises(HTTPException):
        services.user_login(user)


def test_verify_token_user_service(db_session, user_on_db):
    repository = SQLAlchemyUserRepository(db_session, UserModel)
    services = UserServices(repository)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.now(brazilian_timezone) + timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    services.verify_token(access_token)


def test_verify_token_invalid_token_user_service(db_session, user_on_db):
    repository = SQLAlchemyUserRepository(db_session, UserModel)
    services = UserServices(repository)

    data = {
        'sub': user_on_db.username,
        'exp': datetime.now(brazilian_timezone) - timedelta(minutes=30)
    }

    access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    with pytest.raises(HTTPException):
        services.verify_token(access_token)
