from sqlalchemy.orm import Session
from app.repositories.sqlalchemy.repository import SQLAlchemyRepository
from app.db.models import Order as OrderModel
from app.db.models import Check as CheckModel


class SAOrderRepository(SQLAlchemyRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = OrderModel

    def get_check_by_id(self, _id: int):
        return self._db_session.query(CheckModel
                                      ).filter_by(id=_id).one_or_none()
