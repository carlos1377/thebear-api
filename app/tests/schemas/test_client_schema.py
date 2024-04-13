import pytest
from app.schemas.client import Client


def test_client_schema():
    client = Client(
        name='Carlos',
        number='(99) 99999-9999',
        cpf='41683048091'
    )

    assert client.model_dump() == {
        'name': 'Carlos',
        'number': '(99) 99999-9999',
        'cpf': '41683048091'
    }


def test_client_schema_invalid_name():
    with pytest.raises(ValueError):
        client = Client(
            name=1234,
            number='(99) 99999-9999',
            cpf='41683048091'
        )


def test_client_schema_invalid_number():
    with pytest.raises(ValueError):
        client = Client(
            name='carlos',
            number=8899995555,
            cpf='41683048091'
        )


def test_client_schema_invalid_cpf():
    with pytest.raises(ValueError):
        client = Client(
            name='carlos',
            number='(99) 99999-9999',
            cpf=41683048091
        )
