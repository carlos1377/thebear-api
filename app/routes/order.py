from app.services.order_services import OrderServices
from app.routes.deps import order_repository
# from app.routes.deps import get_db_session
from fastapi import Depends, Response, status
from fastapi.routing import APIRouter
from app.schemas.order import Order
# from sqlalchemy.orm import Session


router = APIRouter(prefix='/order')


@router.post('/add')
def create_order(
    order: Order,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    services.create_order(order)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/{_id}')
def get_order(
    _id: int,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order = services.get_order(_id)

    return order


@router.get('/')
def list_orders(
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    orders = services.get_order()

    return orders
