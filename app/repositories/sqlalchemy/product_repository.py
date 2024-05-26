from app.repositories.sqlalchemy.repository import DBRepository
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from sqlalchemy.orm import Session


class DBProductRepository(DBRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = ProductModel

    def _find_category_by_slug(self, slug: str):
        category = self._db_session.query(
            CategoryModel).filter_by(slug=slug).first()

        return category

    def update_object(self, _id: int, _object_dump: dict) -> int:
        category = self._find_category_by_slug(
            _object_dump['category_slug'])

        _object_dump['category_id'] = category.id

        _object_dump.pop('category_slug')

        rows = self._db_session.query(self._model_service).filter_by(
            id=_id).update(_object_dump)

        self._db_session.commit()

        return rows
