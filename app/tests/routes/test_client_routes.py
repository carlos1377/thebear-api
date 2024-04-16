from app.db.models import Client as ClientModel
from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app=app)


def test_add_client_route(db_session):
    body = {
        'name': 'carlos',
        'number': '(99) 99999-9999',
        'cpf': '41683048091'
    }

    response = client.post('/client/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    client_on_db = db_session.query(ClientModel).one_or_none()

    assert client_on_db is not None

    db_session.delete(client_on_db)
    db_session.commit()
