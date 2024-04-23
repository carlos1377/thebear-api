from app.services.order_services import OrderServices
from app.repositories.sqlalchemy.order_repository import SAOrderRepository
from app.schemas.order import Order
import pytest
from fastapi.exceptions import HTTPException


def test_create_order_services(db_session):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order = Order(status=0, mesa=2)

    services.create_order(order)

    order_on_db = services.repository.find_first()

    assert order_on_db is not None

    assert order_on_db.status == order.status.value
    assert order_on_db.mesa == order.mesa

    services.repository.remove(order_on_db)


def test_get_order_by_id_order_services(db_session, order_on_db):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order = services.get_order(order_on_db.id)

    assert order is not None

    assert order.mesa == order_on_db.mesa
    assert order.status == order_on_db.status


def test_get_order_by_id_invalid_id_order_services(db_session):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    with pytest.raises(HTTPException):
        services.get_order(-9)


def test_list_orders_order_services(db_session, orders_on_db):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    orders = services.get_order()

    assert len(orders) == 3

    assert orders[1].mesa == orders_on_db[1].mesa
    assert orders[2].status == orders_on_db[2].status
    assert orders[0].date_time == orders_on_db[2].date_time


def test_update_order_services(db_session, order_on_db):
    order = Order(status=1, mesa=order_on_db.mesa)

    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order_updated = services.update_order(order_on_db.id, order)

    assert order_updated is not None

    assert order_updated.status == order.status.value
    assert order_updated.mesa == order.mesa


def test_update_order_invalid_id_order_services(db_session, order_on_db):
    order = Order(status=1, mesa=order_on_db.mesa)

    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)
    with pytest.raises(HTTPException):
        services.update_order(2, order)


def test_delete_order_services(db_session, order_on_db):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    services.delete_order(order_on_db.id)

    order_deleted = services.repository.id_one_or_none(order_on_db.id)

    assert order_deleted is None
