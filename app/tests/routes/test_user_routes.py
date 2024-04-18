from app.db.models import User as UserModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app=app)


def test_register_user_route(db_session):
    body = {
        'username': 'foo',
        'password': 'bar123!',
        'email': 'foo@bar.com',
        'is_staff': False,
    }

    response = client.post('/user/register', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    user_on_db = db_session.query(UserModel).first()

    assert user_on_db is not None

    db_session.delete(user_on_db)
    db_session.commit()


def test_login_user_route(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'access_token' in data
    assert 'expires_at' in data


def test_login_invalid_username_user_route(user_on_db):
    body = {
        'username': 'invalid',
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_invalid_password_user_route(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'invalid',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
