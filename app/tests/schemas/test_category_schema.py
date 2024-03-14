import pytest
from app.schemas.category import Category


def test_category_schema():
    category = Category(
        name='Bebida',
        slug='bebida'
    )

    assert category.model_dump() == {
        'name': 'Bebida',
        'slug': 'bebida'
    }


def test_category_schema_invalid_values():
    with pytest.raises(ValueError):
        category = Category(
            name='Bebida',
            slug='Bebida'
        )

    with pytest.raises(ValueError):
        category = Category(
            name='Bebida',
            slug='bebida boa'
        )

    with pytest.raises(ValueError):
        category = Category(
            name='Bebida',
            slug='ção'
        )
