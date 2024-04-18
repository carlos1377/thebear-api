from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.client import Client
from app.services.client_services import ClientServices
from app.repositories.sqlalchemy.sqlalchemy_repository import SQLAlchemyRepository
from app.db.models import Client as ClientModel

router = APIRouter(prefix='/client')


@router.post('/add')
def add_clients(
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyRepository(db_session, ClientModel)

    services = ClientServices(repository)

    services.add_client(client=client)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/')
def list_clients(
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients()

    return clients


@router.get('/{_id}')
def list_clients_by_id(
    _id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients(_id)

    return clients


@router.put('/{_id}')
def update_client(
    _id: int,
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    client_in = services.update_client(_id, client)

    return client_in


@router.delete('/{_id}')
def delete_client(
    _id: int,
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.delete_client(_id)

    return Response(status_code=status.HTTP_200_OK)
