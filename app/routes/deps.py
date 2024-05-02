from app.repositories.sqlalchemy.order_repository import SAOrderRepository
from app.repositories.sqlalchemy.check_repository import SACheckRepository
from app.repositories.sqlalchemy.user_repository import SAUserRepository
from app.services.user_services import UserServices
from sqlalchemy.orm import Session as SessionType
from fastapi.security import OAuth2PasswordBearer
from app.db.connection import Session
from fastapi import Depends
import os

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')

TEST_MODE = bool(int(os.environ.get('TEST_MODE', 0)))


def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


def order_repository(
    db_session: SessionType = Depends(get_db_session)
):
    repository = SAOrderRepository(db_session)

    return repository


def check_repository(
    db_session: SessionType = Depends(get_db_session)
):
    repository = SACheckRepository(db_session)

    return repository


def auth(
    db_session: SessionType = Depends(get_db_session),
    token=Depends(oauth_scheme)
):
    if TEST_MODE:
        return

    repository = SAUserRepository(db_session)
    services = UserServices(repository)

    services.verify_token(token)
