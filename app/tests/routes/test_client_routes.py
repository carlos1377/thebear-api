from app.db.models import Client as ClientModel
from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app=app)

header = {'Authorization': 'Bearer token'}

client.headers = header  # type: ignore


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


def test_list_client_route(clients_on_db):
    response = client.get('/client')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[0] == {
        "id": clients_on_db[0].id,
        "name": clients_on_db[0].name,
        "number": clients_on_db[0].number,
        "cpf": clients_on_db[0].cpf,
    }


def test_list_client_by_id_route(clients_on_db):
    _id = clients_on_db[1].id

    response = client.get(f'/client/{_id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "id": clients_on_db[1].id,
        "name": clients_on_db[1].name,
        "number": clients_on_db[1].number,
        "cpf": clients_on_db[1].cpf,
    }


def test_update_client_route(client_on_db):
    _id = client_on_db.id

    body = {
        'name': 'carlos',
        'number': '(99) 99999-9999',
        'cpf': '47545438078'
    }

    response = client.put(f'/client/{_id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "id": _id,
        "name": body['name'],
        "number": body['number'],
        "cpf": body['cpf'],
    }


def test_delete_client_route(client_on_db):
    _id = client_on_db.id

    response = client.delete(f'/client/{_id}')

    assert response.status_code == status.HTTP_200_OK
