from sqlalchemy.orm import Session
from app.repositories.sqlalchemy.repository import SQLAlchemyRepository
from app.db.models import Order as OrderModel


class SAOrderRepository(SQLAlchemyRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = OrderModel
