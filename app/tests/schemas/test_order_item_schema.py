import pytest
from app.schemas.order_item import OrderItem
from app.schemas.order import OrderOutput
from app.schemas.product import ProductOutput
from app.schemas.category import Category


def test_order_item_schema():
    category = Category(name='Bebida', slug='bebida')
    order = OrderOutput(id=1, status='Feito', mesa=1)
    product = ProductOutput(
        id=2, name='Vodka', slug='vodka', price=20,
        stock=40, category=category, description=None,
    )

    order_item = OrderItem(
        product_id=product.id, order_id=order.id,
        quantity=2,
    )

    assert order_item.model_dump() == {
        'product_id': 2,
        'order_id': 1,
        'quantity': 2,
    }


def test_order_item_schema_invalid_product_id():
    with pytest.raises(ValueError):
        order_item = OrderItem(
            product_id='ola', order_id=3,
            quantity=2,
        )


def test_order_item_schema_invalid_order_id():
    with pytest.raises(ValueError):
        order_item = OrderItem(
            product_id=9, order_id=-6,
            quantity=2,
        )


def test_order_item_schema_invalid_quantity():
    with pytest.raises(ValueError):
        order_item = OrderItem(
            product_id=9, order_id=6,
            quantity=5.9,
        )
