import pytest
from app.schemas.product import Product, ProductOutput
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
            price=50,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
            category=category
        )

    with pytest.raises(ValueError):
        category = Category(name='Bebida', slug='bebida')
        product = Product(
            name='Vodka',
            slug='vodka boa',
            price=5,
            stock=10,
            category=category
        )


def test_product_output_schema():
    category = Category(name='Bebida', slug='bebida')
    product_output = ProductOutput(
        id=1,
        name='Vodka',
        slug='vodka-boa',
        price=50,
        stock=10,
        description=None,
        category=category
    )

    assert product_output.model_dump() == {
        'id': 1,
        'name': 'Vodka',
        'slug': 'vodka-boa',
        'price': 50,
        'description': None,
        'stock': 10,
        'category': {
            'name': 'Bebida',
            'slug': 'bebida',
        }
    }
