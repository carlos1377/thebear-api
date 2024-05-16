from fastapi.testclient import TestClient
from app.db.models import Check as CheckModel
from fastapi import status
from app.main import app

client = TestClient(app)

header = {'Authorization': 'Bearer token'}

client.headers = header  # type: ignore


def test_add_check_route(db_session):
    body = {
        'in_use': False
    }

    response = client.post('/checks/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    check_on_db = db_session.query(CheckModel).first()

    db_session.delete(check_on_db)
    db_session.commit()


def test_update_check_route(check_on_db):
    body = {
        'in_use': True
    }

    response = client.put(f'/checks/{check_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': check_on_db.id,
        'in_use': True
    }


def test_get_check_route(check_on_db):
    response = client.get(f'/checks/{check_on_db.id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': check_on_db.id,
        'in_use': check_on_db.in_use,
    }


def test_list_checks_route(checks_on_db):
    response = client.get('/checks/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[0] == {
        'id': checks_on_db[0].id,
        'in_use': checks_on_db[0].in_use,
    }

    assert data[1] == {
        'id': checks_on_db[1].id,
        'in_use': checks_on_db[1].in_use,
    }


def test_delete_check_route(check_on_db):
    response = client.delete(f'/checks/{check_on_db.id}')

    assert response.status_code == status.HTTP_200_OK
