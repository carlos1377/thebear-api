from app.repositories.sqlalchemy.repository import SQLAlchemyRepository
from app.db.models import Client as ClientModel
from app.services.client_services import ClientServices
from app.schemas.client import Client
from fastapi.exceptions import HTTPException
import pytest


def test_add_client_service(db_session):
    client = Client(
        name='carlos',
        number='(99) 99999-9999',
        cpf='41683048091'
    )

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.add_client(client)

    client_on_db = db_session.query(ClientModel).one_or_none()

    assert client_on_db is not None

    assert client_on_db.name == client.name
    assert client_on_db.number == client.number
    assert client_on_db.cpf == client.cpf

    db_session.delete(client_on_db)
    db_session.commit()


def test_list_client_service(db_session, clients_on_db):

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    clients = services.list_clients()

    assert clients is not None
    assert clients[0] == clients_on_db[0]
    assert clients[2].name == clients_on_db[2].name


def test_list_client_by_id_service(db_session, clients_on_db):

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    client = services.list_clients(clients_on_db[0].id)

    assert client is not None
    assert client.name == clients_on_db[0].name


def test_list_client_by_id_invalid_id_service(db_session):

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    with pytest.raises(HTTPException):
        client = services.list_clients(-85)


def test_update_client_service(db_session, client_on_db):

    _id = client_on_db.id
    client = Client(name='Foo Bar',
                    number='(22) 99315-8556', cpf='07751005874')

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.update_client(_id, client)

    client_in = services.repository.id_one_or_none(_id)

    assert client_in.name == client.name
    assert client_in.cpf == client.cpf
    assert client_in.number == client.number


def test_delete_client_service(db_session, client_on_db):

    _id = client_on_db.id

    repository = SQLAlchemyRepository(db_session, ClientModel)
    services = ClientServices(repository)

    services.delete_client(_id)

    client_not_in_db = services.repository.id_one_or_none(_id)

    assert client_not_in_db is None
