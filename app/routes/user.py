from app.repositories.sqlalchemy.user_repository import SAUserRepository  # noqa
from app.schemas.user import (
    FormChangeEmail, User, UserLogin, FormChangePassword)
from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import UserServices
from app.routes.deps import get_db_session
from app.routes.deps import oauth_scheme
from sqlalchemy.orm import Session


router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register')
def user_register(
    user: User,
    db_session: Session = Depends(get_db_session),
):
    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    services.register_user(user)

    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/login')
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    user = UserLogin(
        username=login_request_form.username,
        password=login_request_form.password,
    )

    token_data = services.user_login(user, expires_in=60)

    return token_data


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth_scheme),
):
    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    services.delete_user(user_id, token)

    return Response(status_code=status.HTTP_200_OK)


@router.get('/{username}')
def get_user_by_username(
    username: str,
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth_scheme),
):

    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    user = services.get_user(username, token)

    return user


@router.post('/change-password')
def change_password(
    form: FormChangePassword,
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth_scheme),
):
    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    services.change_password(form.password, form.new_password, token)

    return Response(status_code=status.HTTP_200_OK)


@router.post('/change-email')
def change_email(
    form: FormChangeEmail,
    db_session: Session = Depends(get_db_session),
    token: str = Depends(oauth_scheme),
):
    repository = SAUserRepository(db_session)

    services = UserServices(repository)

    services.change_email(form.password, form.new_email, token)

    return Response(status_code=status.HTTP_200_OK)
