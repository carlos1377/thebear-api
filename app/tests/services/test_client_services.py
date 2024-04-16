from app.db.models import Client as ClientModel
from app.services.client_services import ClientServices
from app.schemas.client import Client


def test_crypt_password_client_service(db_session):
    pass


def test_add_client_service(db_session):
    client = Client(
        name='carlos',
        number='(99) 99999-9999',
        cpf='41683048091'
    )

    services = ClientServices(db_session=db_session)

    services.add_client(client)

    client_on_db = db_session.query(ClientModel).one_or_none()

    assert client_on_db is not None

    assert client_on_db.name == client.name
    assert client_on_db.number == client.number
    assert client_on_db.cpf == client.cpf

    db_session.delete(client_on_db)
    db_session.commit()


def test_list_client_service(db_session, clients_on_db):
    services = ClientServices(db_session=db_session)

    clients = services.list_clients()

    assert clients is not None
    assert clients[0] == clients_on_db[0]
    assert clients[2].name == clients_on_db[2].name


def test_list_client_by_id_service(db_session, clients_on_db):
    services = ClientServices(db_session=db_session)

    client = services.list_clients(clients_on_db[0].id)

    assert client is not None
    assert client.name == clients_on_db[0].name
