from app.db.models import OrderItem as OrderItemModel
from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
from app.db.models import Client as ClientModel
from app.db.models import Check as CheckModel
from app.db.models import Order as OrderModel
from app.db.models import User as UserModel
from passlib.context import CryptContext
from app.db.connection import Session
from sqlalchemy.orm import Session as SessionTyping
from typing import Generator
import pytest

crypt_context = CryptContext(schemes=['sha256_crypt'])


def check_if_is_deleted(model, _object, _db_session):
    _object_on_db = _db_session.query(model) \
        .filter_by(id=_object.id).one_or_none()

    if _object_on_db is None:
        return False
    return True


@pytest.fixture()
def db_session() -> Generator[SessionTyping, None, None]:
    try:
        session: SessionTyping = Session()
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
        still_on_db = check_if_is_deleted(CategoryModel, category, db_session)
        if still_on_db:
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

    still_on_db = check_if_is_deleted(CategoryModel, category, db_session)
    if still_on_db:
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

    still_on_db = check_if_is_deleted(ProductModel, product, db_session)
    if still_on_db:
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

    still_on_db = check_if_is_deleted(ClientModel, client, db_session)
    if still_on_db:
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
        still_on_db = check_if_is_deleted(ClientModel, client, db_session)
        if still_on_db:
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

    still_on_db = check_if_is_deleted(UserModel, user, db_session)
    if still_on_db:
        db_session.delete(user)
        db_session.commit()


@pytest.fixture()
def user_staff_on_db(db_session):
    user = UserModel(username='main',
                     password=crypt_context.hash('pass123!'),
                     email='main@cto.com', is_staff=True
                     )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    yield user

    still_on_db = check_if_is_deleted(UserModel, user, db_session)
    if still_on_db:
        db_session.delete(user)
        db_session.commit()


@pytest.fixture()
def order_on_db(db_session):
    order = OrderModel(status=0, mesa=13)

    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)

    yield order

    still_on_db = check_if_is_deleted(OrderModel, order, db_session)
    if still_on_db:
        db_session.delete(order)
        db_session.commit()


@pytest.fixture()
def orders_on_db(db_session):
    orders = [
        OrderModel(status=status, mesa=mesa)
        for status, mesa in [(1, 5), (0, 10), (3, 18)]
    ]

    db_session.add_all(orders)
    db_session.commit()

    for order in orders:
        db_session.refresh(order)

    yield orders

    for order in orders:
        still_on_db = check_if_is_deleted(OrderModel, order, db_session)
        if still_on_db:
            db_session.delete(order)
            db_session.commit()
    db_session.flush()


@pytest.fixture()
def check_on_db(db_session):
    check = CheckModel(in_use=False)

    db_session.add(check)
    db_session.commit()
    db_session.refresh(check)

    yield check

    db_session.delete(check)
    db_session.commit()


@pytest.fixture()
def checks_on_db(db_session):
    checks = [
        CheckModel(in_use=use)
        for use in [True, False]
    ]

    db_session.add_all(checks)
    db_session.commit()
    for check in checks:
        db_session.refresh(check)

    yield checks

    for check in checks:
        still_on_db = check_if_is_deleted(CheckModel, check, db_session)
        if still_on_db:
            db_session.delete(check)
            db_session.commit()
    db_session.flush()


# @pytest.fixture()
# def order_item_on_db(db_session, product_on_db, order_on_db, client_on_db):
#     order_item = OrderItemModel(
#         client_id=client_on_db.id,
#         product_id=product_on_db.id,
#         order_id=order_on_db.id,
#         quantity=3,
#     )

#     db_session.add(order_item)
#     db_session.commit()
#     db_session.refresh(order_item)

#     yield order_item

#     still_on_db = check_if_is_deleted(OrderItemModel, order_item, db_session)
#     if still_on_db:
#         db_session.delete(order_item)
#         db_session.commit()
