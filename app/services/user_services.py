from app.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository  # noqa
from app.schemas.user import User, TokenData, UserLogin, UserOutput
from fastapi.exceptions import HTTPException
from app.db.models import User as UserModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import status
import pytz
import os

crypt_context = CryptContext(schemes=['sha256_crypt'])

SECRET_KEY = os.environ.get('SECRET_KEY', '')
ALGORITHM = os.environ.get('ALGORITHM', '')

brazilian_timezone = pytz.timezone('America/Sao_Paulo')


class UserServices:
    def __init__(self, repository: SQLAlchemyUserRepository) -> None:
        self.repository = repository

    def register_user(self, user: User):
        user_is_on_db = self.repository.get_by_username(user.username)

        if user_is_on_db is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'User {user.username} already exists'
            )

        user_model = UserModel(
            **user.model_dump(exclude={'password'}),
            password=crypt_context.hash(user.password)
        )
        self.repository.save(user_model)

    def user_login(self, user: UserLogin, expires_in: int = 30):
        user_on_db = self.repository.get_by_username(user.username)

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Username or password does not exist',
            )

        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Username or password does not exist',
            )

        expires_at = datetime.now(brazilian_timezone) + \
            timedelta(minutes=expires_in)

        data = {
            'sub': user_on_db.username,
            'exp': expires_at,
        }

        access_token = jwt.encode(data, SECRET_KEY, ALGORITHM)

        token_data = TokenData(access_token=access_token,
                               expires_at=expires_at)

        return token_data

    def verify_token(self, token: str):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )

        user_on_db = self.repository.get_by_username(data['sub'])

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )

    def delete_user(self, user_id: int, token: str):
        self._verify_permission(token)

        user_to_delete = self.repository.id_one_or_none(user_id)

        if user_to_delete is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )

        self.repository.remove(user_to_delete)

    def _verify_permission(self, token: str):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )

        user = self.repository.get_by_username(data['sub'])

        if not user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You don't have permission to this action"
            )

    def _verify_permission_change_yourself(self, token: str) -> int:
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid Token'
            )

        user = self.repository.get_by_username(data['sub'])

        return user.id

    def get_user(self, username: str, token: str):
        self._verify_permission(token)

        user = self.repository.get_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} not found"
            )

        user_output = UserOutput(
            username=user.username,
            email=user.email,
            id=user.id,
            is_staff=user.is_staff,
        )

        return user_output

    def change_password(self, password, new_password, token):
        user_id = self._verify_permission_change_yourself(token)

        user_to_update = self.repository.id_one_or_none(user_id)

        if user_to_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not crypt_context.verify(password, user_to_update.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        user_to_update.password = crypt_context.hash(new_password)
        self.repository.save(user_to_update)

    def change_email(self, password, new_email, token):
        user_id = self._verify_permission_change_yourself(token)

        user_to_update = self.repository.id_one_or_none(user_id)

        if user_to_update is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if not crypt_context.verify(password, user_to_update.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )

        user_to_update.email = new_email
        self.repository.save(user_to_update)
