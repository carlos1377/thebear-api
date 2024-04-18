import pytest
from app.db.connection import Session
from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
from app.db.models import Client as ClientModel
from app.db.models import User as UserModel
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['sha256_crypt'])


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


@pytest.fixture()
def category_on_db(db_session):
    category = CategoryModel(name='Foo', slug='bar')

    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    db_session.flush()

    yield category

    db_session.delete(category)
    db_session.commit()


@pytest.fixture()
def product_on_db(db_session, category_on_db):
    product = ProductModel(
        name='Heineken', slug='heineken',
        price=12.99, description='', stock=10,
        category_id=category_on_db.id
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    yield product

    db_session.delete(product)
    db_session.commit()


@pytest.fixture()
def client_on_db(db_session):
    client = ClientModel(
        name='foo bar',
        number='(99) 99999-9999',
        cpf='41683048091'
    )

    db_session.add(client)
    db_session.commit()
    db_session.refresh(client)

    yield client

    db_session.delete(client)
    db_session.commit()


@pytest.fixture()
def clients_on_db(db_session):
    clients = [
        ClientModel(name='Foo Bar',
                    number='(22) 99315-8556', cpf='07751005874'),
        ClientModel(name='Carlos Fancy',
                    number='(68) 99684-1827', cpf='26764931836'),
        ClientModel(name='Richard Wesley',
                    number='(92) 99671-4167', cpf='00180827855'),
    ]

    for client in clients:
        db_session.add(client)

    db_session.commit()

    for client in clients:
        db_session.refresh(client)

    yield clients

    for client in clients:
        db_session.delete(client)

    db_session.commit()
    db_session.flush()


@pytest.fixture()
def user_on_db(db_session):
    user = UserModel(username='foo',
                     password=crypt_context.hash('pass123!'),
                     email='foo@bar.com', is_staff=False
                     )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield user

    db_session.delete(user)
    db_session.commit()
