from app.repositories.sqlalchemy.repository import SQLAlchemyRepository  # noqa
from fastapi import APIRouter, Depends, Response, status
from app.services.client_services import ClientServices
from app.routes.deps import get_db_session, auth
from app.db.models import Client as ClientModel
from app.schemas.client import Client
from sqlalchemy.orm import Session

router = APIRouter(prefix='/client', dependencies=[Depends(auth)])


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
