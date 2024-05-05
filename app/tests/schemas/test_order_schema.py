from app.schemas.order import Order, OrderPartial, OrderItem, OrderOutput
from app.schemas.category import CategoryOutput
from app.schemas.product import ProductOutput
from app.schemas.check import CheckOutput
from datetime import datetime
import pytest


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
        Order(
            status='Em preparo',
            check_id=2
        )


def test_order_schema_invalid_check_id():
    with pytest.raises(ValueError):
        Order(
            status=0,
            check_id=-8
        )


def test_order_partial_schema():
    order = OrderPartial(status=2)

    assert order.model_dump(mode='json') == {
        'status': 2,
    }


def test_order_output_schema():
    date_now = datetime.now().strftime("%Y-%m-%dT%X")
    check = CheckOutput(in_use=True, id=4)

    category = CategoryOutput(id=2, name='Bebida', slug='bebida')

    product_output = ProductOutput(
        id=1, name='Vodka', slug='vodka-boa',
        price=50, stock=10, description=None, category=category
    )

    order_item = OrderItem(product=product_output, quantity=2)

    order_output = OrderOutput(
        id=1, date_time=date_now, status=1,
        check_id=check.id, order_items=[order_item]
    )

    assert order_output.model_dump(mode='json') == {
        'id': 1,
        'date_time': date_now,
        'status': 1,
        'check_id': 4,
        'order_items': [
            {
                'product': {
                    'id': 1,
                    'name': 'Vodka',
                    'slug': 'vodka-boa',
                    'price': 50.0,
                    'description': None,
                    'stock': 10,
                    'category': {
                        'id': 2,
                        'name': 'Bebida',
                        'slug': 'bebida'
                    }
                },
                'quantity': 2,
            }
        ]
    }
