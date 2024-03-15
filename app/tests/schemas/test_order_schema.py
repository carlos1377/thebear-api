import pytest
from app.schemas.order import Order


def test_order_schema():
    order = Order(
        status='Em andamento',
        mesa=9
    )

    assert order.model_dump() == {
        'status': 'Em andamento',
        'mesa': 9,
    }


def test_order_schema_invalid_status():
    with pytest.raises(ValueError):
        order = Order(
            status=10,
            mesa=10,
        )


def test_order_schema_invalid_mesa():
    with pytest.raises(ValueError):
        order = Order(
            status='Em andamento',
            mesa='MESA01',
        )
