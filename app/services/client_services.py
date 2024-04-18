from fastapi.exceptions import HTTPException
from app.db.models import Client as ClientModel
from app.schemas.client import Client
from fastapi import status
from app.repositories.base import Repository


class ClientServices:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository  # Instancia o repositório

    def add_client(self, client: Client):
        client_model = ClientModel(**client.model_dump())

        self.repository.save(client_model)

    def list_clients(self, _id: int | None = None):
        if _id is None:
            clients_on_db = self.repository.get_all()
            return clients_on_db

        client_on_db = self.repository.id_one_or_none(_id)

        if client_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Client {_id} not found'
            )

        return client_on_db

    def update_client(self, _id: int, client: Client):
        client_dump = client.model_dump()

        rows = self.repository.update_object(
            _id, client_dump)

        if rows == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Client {_id} not found'
            )

        client_dump['id'] = _id
        return client_dump

    def delete_client(self, _id: int):
        client = self.repository.id_one_or_none(_id)

        self.repository.remove(client)
