import pytest
from app.schemas.product import Product
from app.schemas.category import Category


def test_product_schema():
    category = Category(name='Bebida', slug='bebida')
    product = Product(
        name='Vodka',
        slug='vodka',
        price=10.5,
        description='Lorem Ipsum Dolor Amet',
        stock=10,
        category=category
    )

    assert product.model_dump() == {
        'name': 'Vodka',
        'slug': 'vodka',
        'price': 10.5,
        'description': 'Lorem Ipsum Dolor Amet',
        'stock': 10,
        'category': {
            'name': 'Bebida',
            'slug': 'bebida',
        }
    }


def test_product_schema_invalid_category():
    with pytest.raises(ValueError):
        product = Product(
            name='Vodka',
            slug='vodka',
            price=10.5,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
            category='Bebida'
        )


def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        category = Category(name='Bebida', slug='bebida')
        product = Product(
            name='Vodka',
            slug='vodka',
            price=0,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
            category=category
        )


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        category = Category(name='Bebida', slug='bebida')
        product = Product(
            name='Vodka',
            slug='Vodka',
            price=0,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
            category=category
        )

    with pytest.raises(ValueError):
        category = Category(name='Bebida', slug='bebida')
        product = Product(
            name='Vodka',
            slug='vodka boa',
            price=0,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
            category=category
        )
