from sqlalchemy.orm import Session
from app.db.repository import Repository


class SQLAlchemyRepository(Repository):
    def __init__(self, db_session: Session, model_service) -> None:
        self.db_session = db_session
        self.model_service = model_service

    def get_all(self) -> list:
        return self.db_session.query(self.model_service).all()

    def id_one_or_404(self, _id: int):
        _object = self.db_session.query(
            self.model_service).filter_by(id=_id).one_or_none()
        return _object

    def save(self, _object) -> None:
        self.db_session.add(_object)
        self.db_session.commit()

    def remove(self, _object) -> None:
        self.db_session.delete(_object)
        self.db_session.commit()

    def update_object(self, _id: int, _object_dump: dict) -> int:
        rows = self.db_session.query(self.model_service).filter_by(
            id=_id).update(_object_dump)

        self.db_session.commit()

        return rows
