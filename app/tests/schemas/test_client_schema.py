import pytest
from app.schemas.client import Client


def test_client_schema():
    client = Client(
        name='Carlos',
        email='carlos@email.com',
        number='(99) 99999-9999',
        password='1234'
    )

    assert client.model_dump() == {
        'name': 'Carlos',
        'email': 'carlos@email.com',
        'number': '(99) 99999-9999',
        'password': '1234'
    }


def test_client_schema_invalid_name():
    with pytest.raises(ValueError):
        client = Client(
            name=1234,
            email='carlos@email.com',
            number=None,
            password='1234'
        )


def test_client_schema_invalid_email():
    with pytest.raises(ValueError):
        client = Client(
            name='carlos',
            email='carlos',
            number='(99) 99999-9999',
            password='1234'
        )


def test_client_schema_invalid_number():
    with pytest.raises(ValueError):
        client = Client(
            name='carlos',
            email='carlos@email.com',
            number=8899995555,
            password='1234'
        )


def test_client_schema_invalid_password():
    with pytest.raises(ValueError):
        client = Client(
            name='carlos',
            email='carlos@email.com',
            number='(99) 99999-9999',
            password=None
        )
