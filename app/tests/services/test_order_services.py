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
        order = services.get_order(-9)
