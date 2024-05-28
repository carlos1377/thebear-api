from app.repositories.sqlalchemy.repository import DBRepository  # noqa
from fastapi import APIRouter, Depends, Response, status
from app.services.client_services import ClientServices
from app.schemas.client import Client, ClientOutput
from app.routes.deps import get_db_session, auth
from app.db.models import Client as ClientModel
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/clients', dependencies=[Depends(auth)], tags=['Clients'])


@router.post(
    '/add', description='Create a client', response_model=ClientOutput)
def add_clients(
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)

    services = ClientServices(repository)

    client_added = services.add_client(client=client).model_dump_json()

    return Response(client_added,
                    status_code=status.HTTP_201_CREATED, media_type="json")


@router.get(
    '/', description='List all clients', response_model=list[ClientOutput])
def list_clients(
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients()

    return clients


@router.get(
    '/{id}', description='List one client', response_model=ClientOutput)
def list_clients_by_id(
    id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients(id)

    return clients


@router.put(
    '/{id}', description='Update a client', response_model=ClientOutput)
def update_client(
    id: int,
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    client_in = services.update_client(id, client)

    return client_in


@router.delete(
    '/{id}', description='Delete a client')
def delete_client(
    id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = DBRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.delete_client(id)

    return Response(status_code=status.HTTP_200_OK)
