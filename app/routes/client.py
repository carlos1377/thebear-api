from app.repositories.sqlalchemy.repository import DBRepository  # noqa
from fastapi import APIRouter, Depends, Response, status
from app.services.client_services import ClientServices
from app.routes.deps import get_db_session, auth
from app.db.models import Client as ClientModel
from app.schemas.client import Client
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/clients', dependencies=[Depends(auth)], tags=['Clients'])


@router.post('/add')
def add_clients(
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)

    services = ClientServices(repository)

    client_added = services.add_client(client=client).model_dump_json()

    return Response(client_added, status_code=status.HTTP_201_CREATED)


@router.get('/')
def list_clients(
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients()

    return clients


@router.get('/{id}')
def list_clients_by_id(
    id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients(id)

    return clients


@router.put('/{id}')
def update_client(
    id: int,
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    client_in = services.update_client(id, client)

    return client_in


@router.delete('/{id}')
def delete_client(
    id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.delete_client(id)

    return Response(status_code=status.HTTP_200_OK)
