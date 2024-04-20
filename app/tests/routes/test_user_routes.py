from app.db.models import User as UserModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app=app)

# TODO: Create function to login and DRY on routes that need login


def test_register_user_route(db_session):
    body = {
        'username': 'fooo',
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


def test_get_user_by_username_route(user_on_db, user_staff_on_db):
    body = {
        'username': user_staff_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get(f'/user/{user_on_db.username}', headers=headers)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': user_on_db.id,
        'username': user_on_db.username,
        'email': user_on_db.email,
        'is_staff': user_on_db.is_staff,
    }


def test_delete_user_route(user_staff_on_db, user_on_db):
    body = {
        'username': user_staff_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    token = response.json()

    access_token = token['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.delete(f'/user/{user_on_db.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_get_user_by_username_invalid_username_route(user_on_db, user_staff_on_db):
    body = {
        'username': user_staff_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/user/jacare', headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_change_password_user_route(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}

    body = {
        'password': 'pass123!',
        'confirm_password': 'pass123!',
        'new_password': 'Pass123!@',
    }

    response = client.post('/user/change-password', json=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK


def test_change_email_user_route(user_on_db):
    body = {
        'username': user_on_db.username,
        'password': 'pass123!',
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = client.post('/user/login', data=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    access_token = response.json()['access_token']

    headers = {'Authorization': f'Bearer {access_token}'}

    body = {
        'password': 'pass123!',
        'confirm_password': 'pass123!',
        'new_email': 'foo@bar.com',
    }

    response = client.post('/user/change-email', json=body, headers=headers)

    assert response.status_code == status.HTTP_200_OK
