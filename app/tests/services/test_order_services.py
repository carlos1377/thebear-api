from app.repositories.sqlalchemy.order_repository import DBOrderRepository
from app.services.order_services import OrderServices, OrderItemServices
from app.schemas.order import Order, OrderPartial, OrderItemInput
from fastapi.exceptions import HTTPException
import pytest


def test_create_order_services(db_session, check_on_db):
    _id_check_db = check_on_db.id
    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)

    order = Order(status=0, check_id=_id_check_db)

    services.create_order(order)

    order_on_db = services.repository.find_first()

    assert order_on_db is not None

    assert order_on_db.status == order.status.value
    assert order_on_db.check_id == order.check_id

    services.repository.remove(order_on_db)


def test_update_order_services(db_session, order_on_db):
    order = Order(status=1, check_id=order_on_db.check_id)

    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)

    order_updated = services.update_order(order_on_db.id, order)

    assert order_updated is not None

    assert order_updated.status.value == order.status.value
    assert order_updated.check_id == order.check_id


def test_update_order_invalid_id_order_services(db_session, order_on_db):
    order = Order(status=1, check_id=order_on_db.check_id)

    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)
    with pytest.raises(HTTPException):
        services.update_order(2, order)


def test_delete_order_services(db_session, order_on_db):
    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)

    services.delete_order(order_on_db.id)

    order_deleted = services.repository.id_one_or_none(order_on_db.id)

    assert order_deleted is None


def test_partial_update_order_services(db_session, order_on_db):
    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)

    new_status = OrderPartial(status=1)

    order = services.update_status(order_on_db.id, new_status)

    assert order.status.value == new_status.status.value


def test_create_order_item_order_services(
    db_session, product_on_db, order_on_db
):
    repository = DBOrderRepository(db_session)
    services = OrderItemServices(repository)

    order_item = OrderItemInput(product_id=product_on_db.id, quantity=1)

    services.create_item(order_on_db.id, order_item)

    order_items_on_db = services.repository.get_all_order_items_by_order_id(
        order_on_db.id)

    assert len(order_items_on_db) > 0
    assert order_items_on_db[0].product_id == product_on_db.id
    assert order_items_on_db[0].quantity == 1

    services.repository.remove_all(order_items_on_db)


def test_get_order_items_order_services(db_session, order_items_on_db):
    repository = DBOrderRepository(db_session)
    services = OrderItemServices(repository)

    order_item_frst = services.get_order_items(order_items_on_db[0].order_id)
    order_item_scnd = services.get_order_items(order_items_on_db[1].order_id)

    assert order_item_frst[0].product.id == order_items_on_db[0].product_id
    assert order_item_scnd[1].quantity == order_items_on_db[1].quantity


def test_get_all_orders_services(db_session, order_items_on_db):
    repository = DBOrderRepository(db_session)
    services = OrderServices(repository)

    orders = services.get_all_orders()

    assert orders is not None
    assert isinstance(orders, list)

    assert orders[0].id == order_items_on_db[0].order_id
    assert orders[0].order_items[0].quantity == order_items_on_db[0].quantity


def test_update_quantity_order_item_services(db_session, order_item_on_db):
    order_id, product_id = order_item_on_db.order_id, order_item_on_db.product_id  # noqa
    repository = DBOrderRepository(db_session)
    services = OrderItemServices(repository)

    order_item = services.update_quantity_order_item(order_id, product_id, 9)

    assert order_item.quantity == 9

    order_item_updated = services.repository.get_order_item_by_ids(
        order_id, product_id)

    assert order_item_updated.quantity == 9


def test_delete_order_item_services(db_session, order_item_on_db):
    order_id, product_id = order_item_on_db.order_id, order_item_on_db.product_id  # noqa
    repository = DBOrderRepository(db_session)
    services = OrderItemServices(repository)

    order_item_deleted = services.delete_order_item(order_id, product_id)

    order_item_deleted_db = services.repository.get_order_item_by_ids(
        order_id, product_id)

    assert order_item_deleted_db is None

    assert order_item_deleted.product.id == product_id
    assert order_item_deleted.quantity == order_item_on_db.quantity
