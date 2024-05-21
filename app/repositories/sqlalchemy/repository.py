from sqlalchemy.orm import Session
from app.repositories.base import Repository

# TODO: REFATORAR REPOSITORIOS, RECEBER REPOSITORIO AO INVES DE DB_SESSIONS
# TODO: UM REPOSITORIO PARA CADA MODEL


class DBRepository(Repository):
    def __init__(self, db_session: Session, model_service) -> None:
        self._db_session = db_session
        self._model_service = model_service

    def get_all(self) -> list:
        return self._db_session.query(self._model_service).all()

    def id_one_or_none(self, _id: int):
        _object = self._db_session.query(
            self._model_service).filter_by(id=_id).one_or_none()
        return _object

    def save(self, _object):
        self._db_session.add(_object)
        self._db_session.commit()
        self._db_session.refresh(_object)

        return _object.id

    def remove(self, _object) -> None:
        self._db_session.delete(_object)
        self._db_session.commit()

    def update_object(self, _id: int, _object_dump: dict) -> int:
        rows = self._db_session.query(self._model_service).filter_by(
            id=_id).update(_object_dump)

        self._db_session.commit()

        return rows

    def find_first(self):
        _object = self._db_session.query(self._model_service).first()

        return _object
