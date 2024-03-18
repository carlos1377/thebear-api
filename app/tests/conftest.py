import pytest
from app.db.connection import Session
from app.db.models import Category as CategoryModel


@pytest.fixture()
def db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()


@pytest.fixture()
def categories_on_db(db_session):
    categories = [
        CategoryModel(name='Bebida', slug='bebida'),
        CategoryModel(name='Comida Quente', slug='comida-quente'),
        CategoryModel(name='Comida Fria', slug='comida-fria'),
        CategoryModel(name='Bebida sem Alcool', slug='bebida-sem-alcool'),
    ]

    for category in categories:
        db_session.add(category)

    db_session.commit()

    for category in categories:
        db_session.refresh(category)

    yield categories

    for category in categories:
        db_session.delete(category)

    db_session.commit()
