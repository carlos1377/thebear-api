from app.repositories.sqlalchemy.user_repository import SAUserRepository  # noqa
from app.services.user_services import UserServices
from sqlalchemy.orm import Session as SessionType
from fastapi.security import OAuth2PasswordBearer
from app.db.models import User as UserModel
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


def auth(
    db_session: SessionType = Depends(get_db_session),
    token=Depends(oauth_scheme)
):
    if TEST_MODE:
        return

    repository = SAUserRepository(db_session, UserModel)
    services = UserServices(repository)

    services.verify_token(token)
