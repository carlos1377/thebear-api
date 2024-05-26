from app.repositories.sqlalchemy.repository import DBRepository
from app.db.models import Category as CategoryModel
from sqlalchemy.orm import Session


class DBCategoryRepository(DBRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = CategoryModel
