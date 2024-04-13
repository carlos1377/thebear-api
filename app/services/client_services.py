from app.schemas.client import Client
from sqlalchemy.orm import Session
from app.db.models import Client as ClientModel
import bcrypt


class ClientServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    @staticmethod
    def encrypt_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(password.encode(), salt)

        return hashed_password

    def check_password(self, password: str, _id: int) -> bool:
        client = self.db_session.query(ClientModel).filter_by(id=_id).one_or_none()

        if client is None:
            return False

        check = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=client.password
        )

        return check
