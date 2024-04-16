from app.schemas.client import Client
from sqlalchemy.orm import Session
from app.db.models import Client as ClientModel
from fastapi.exceptions import HTTPException
from fastapi import status


class ClientServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add_client(self, client: Client) -> None:
        client_model = ClientModel(**client.model_dump())

        self.db_session.add(client_model)
        self.db_session.commit()
        self.db_session.refresh(client_model)

    def list_clients(self, id: int | None = None):
        if id is None:
            clients_on_db = self.db_session.query(ClientModel).all()
            return clients_on_db
        client_on_db = self.db_session.query(
            ClientModel).filter_by(id=id).one_or_none()

        if client_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Client {id} not found',
            )

        return client_on_db
