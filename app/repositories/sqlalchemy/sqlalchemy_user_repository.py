from app.db.models import User as UserModel
from app.repositories.sqlalchemy.sqlalchemy_repository import (
    SQLAlchemyRepository
)


class SQLAlchemyUserRepository(SQLAlchemyRepository):

    def get_by_username(self, username: str):
        user = self._db_session.query(UserModel).filter_by(
            username=username).one_or_none()

        return user
