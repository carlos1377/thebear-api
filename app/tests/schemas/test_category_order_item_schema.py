import pytest
# from app.schemas.order_item import OrderItem
from app.schemas.order import OrderOutput
from app.schemas.product import ProductOutput
from app.schemas.category import Category


def test_order_item_schema():
    category = Category(name='Bebida', slug='bebida')
    order = OrderOutput(id=1, status='Feito', mesa=1)
    product = ProductOutput(
        id=2, name='Vodka', slug='vodka', price=20,
        stock=40, category=category
    )
