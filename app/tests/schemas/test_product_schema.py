from app.schemas.product import Product, ProductOutput, ProductInput
from app.schemas.category import Category, CategoryOutput
import pytest


def test_product_schema():
    product = Product(
        name='Vodka',
        slug='vodka',
        price=10.5,
        description='Lorem Ipsum Dolor Amet',
        stock=10,
    )

    assert product.model_dump() == {
        'name': 'Vodka',
        'slug': 'vodka',
        'price': 10.5,
        'description': 'Lorem Ipsum Dolor Amet',
        'stock': 10,
    }


def test_product_schema_invalid_price():
    with pytest.raises(ValueError):
        product = Product(
            name='Vodka',
            slug='vodka',
            price=0,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
        )


def test_product_schema_invalid_slug():
    with pytest.raises(ValueError):
        product = Product(
            name='Vodka',
            slug='Vodka',
            price=50,
            description='Lorem Ipsum Dolor Amet',
            stock=10,
        )

    with pytest.raises(ValueError):
        product = Product(
            name='Vodka',
            slug='vodka boa',
            price=5,
            stock=10,
        )


def test_product_output_schema():
    category = CategoryOutput(id=2, name='Bebida', slug='bebida')
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
            'id': 2,
            'name': 'Bebida',
            'slug': 'bebida'
        }
    }


def test_product_output_schema_invalid_category():
    with pytest.raises(ValueError):
        product_output = ProductOutput(
            id=1,
            name='Vodka',
            slug='vodka-boa',
            price=50,
            stock=10,
            description=None,
            category='oi'
        )


def test_product_input_schema():
    category = Category(name='Bebida', slug='bebida')
    product_input = ProductInput(
        name='Vodka',
        slug='vodka-boa',
        price=50,
        stock=10,
        description=None,
        category_slug=category.slug
    )

    assert product_input.model_dump() == {
        'name': 'Vodka',
        'slug': 'vodka-boa',
        'price': 50,
        'description': None,
        'stock': 10,
        'category_slug': 'bebida'
    }
