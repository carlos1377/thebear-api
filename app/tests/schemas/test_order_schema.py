import pytest
from app.schemas.order import Order


def test_order_schema():
    order = Order(
        status=1,
        check_id=2
    )

    # Quando for fazer dumop do modelo, usar mode='json', para
    # serializar o enum como int
    assert order.model_dump(mode='json') == {
        'status': 1,
        'check_id': 2
    }


def test_order_schema_invalid_status():
    with pytest.raises(ValueError):
        order = Order(
            status='Em preparo',
            check_id=2
        )


def test_order_schema_invalid_check_id():
    with pytest.raises(ValueError):
        order = Order(
            status=0,
            check_id=-8
        )
