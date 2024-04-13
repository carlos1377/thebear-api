from app.db.models import Client as ClientModel
from app.services.client_services import ClientServices
from app.schemas.client import Client

def test_add_client_service(db_session):
    client = Client(
            name='carlos',
            email='carlos@email.com',
            number='(99) 99999-9999',
            password='1234'
    )

    services = ClientServices(db_session=db_session)
    
    services.add_client(client)

    client_on_db = db_session.query(ClientModel).one_or_none()

    assert client_on_db is not None

    assert client_on_db.name == client.name
    assert client_on_db.email == client.email
    assert client_on_db.number == client.number
    assert client_on_db.password == client.password

