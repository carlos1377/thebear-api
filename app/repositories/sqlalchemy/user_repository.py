from sqlalchemy.orm import Session
from app.db.models import User as UserModel
from app.repositories.sqlalchemy.repository import SQLAlchemyRepository


class SQLAlchemyUserRepository(SQLAlchemyRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = UserModel

    def get_by_username(self, username: str):
        user = self._db_session.query(UserModel).filter_by(
            username=username).one_or_none()

        return user
