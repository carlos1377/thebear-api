from app.repositories.sqlalchemy.repository import DBRepository
from app.db.models import Check as CheckModel
from sqlalchemy.orm import Session


class DBCheckRepository(DBRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = CheckModel
