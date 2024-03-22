import pytest
from app.schemas.category import Category, CategoryOutput


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


def test_category_output_schema():
    category = CategoryOutput(
        name='Bebida',
        slug='bebida',
        id=2,
    )

    assert category.model_dump() == {
        'name': 'Bebida',
        'slug': 'bebida',
        'id': 2,
    }


def test_category_output_schema_invalid_id():
    with pytest.raises(ValueError):
        category = CategoryOutput(
            name='Bebida',
            slug='bebida',
            id='str',
        )
