from app.repositories.sqlalchemy.order_repository import SAOrderRepository
from app.services.order_services import OrderServices
from app.schemas.order import Order, OrderPartial, OrderItemInput
from fastapi.exceptions import HTTPException
import pytest
from pprint import pprint


def test_create_order_services(db_session, check_on_db):
    _id_check_db = check_on_db.id
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order = Order(status=0, check_id=_id_check_db)

    services.create_order(order)

    order_on_db = services.repository.find_first()

    assert order_on_db is not None

    assert order_on_db.status == order.status.value
    assert order_on_db.check_id == order.check_id

    services.repository.remove(order_on_db)


def test_get_order_by_id_order_services(db_session, order_on_db):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order = services.get_order(order_on_db.id)

    assert order is not None

    assert order.check_id == order_on_db.check_id
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

    assert orders[1].check_id == orders_on_db[1].check_id
    assert orders[2].status == orders_on_db[2].status
    assert orders[0].date_time == orders_on_db[0].date_time


def test_update_order_services(db_session, order_on_db):
    order = Order(status=1, check_id=order_on_db.check_id)

    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order_updated = services.update_order(order_on_db.id, order)

    assert order_updated is not None

    assert order_updated.status == order.status.value
    assert order_updated.check_id == order.check_id


def test_update_order_invalid_id_order_services(db_session, order_on_db):
    order = Order(status=1, check_id=order_on_db.check_id)

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


def test_partial_update_order_services(db_session, order_on_db):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    new_status = OrderPartial(status=1)

    order = services.update_status(order_on_db.id, new_status)

    assert order.status == new_status.status.value


def test_create_order_item_order_services(
    db_session, product_on_db, order_on_db
):
    repository = SAOrderRepository(db_session)
    services = OrderServices(repository)

    order_item = OrderItemInput(product_id=product_on_db.id, quantity=1)

    services.create_item(order_on_db.id, order_item)

    order_items_on_db = services.repository.get_all_order_items_by_order_id(
        order_on_db.id)

    assert len(order_items_on_db) > 0
    assert order_items_on_db[0].product_id == product_on_db.id
    assert order_items_on_db[0].quantity == 1

    services.repository.remove_all(order_items_on_db)
