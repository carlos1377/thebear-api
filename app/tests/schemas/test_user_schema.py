from app.schemas.user import User
import pytest


def test_user_schema():
    user = User(
        username='corso',
        password='password',
        email='carlos@email.com',
        is_staff=False,
    )

    assert user.model_dump() == {
        'username': 'corso',
        'password': 'password',
        'email': 'carlos@email.com',
        'is_staff': False
    }


def test_user_schema_invalid_username():
    with pytest.raises(ValueError):
        user = User(
            username=1234,
            password='password',
            email='carlos@email.com',
            is_staff=False,
        )


def test_user_schema_invalid_password():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password={'foo': 'bar'},
            email='carlos@email.com',
            is_staff=False,
        )


def test_user_schema_invalid_email():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password='password',
            email='carlos@email',
            is_staff=False,
        )


def test_user_schema_invalid_is_staff():
    with pytest.raises(ValueError):
        user = User(
            username='corso',
            password='password',
            email='carlos@email.com',
            is_staff=None
        )
