from app.services.order_services import OrderServices, OrderItemServices
from app.schemas.order import (
    Order, OrderPartial, OrderItemInput, OrderItemPartial
)
from app.routes.deps import order_repository
from fastapi import Depends, Response, status
from fastapi.routing import APIRouter

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
def get_order_output(
    _id: int,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_output = services.serializer.serialize_order_output(_id)

    return order_output


@router.get('s/')
def get_all_orders(
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    orders = services.get_all_orders()

    return orders


@router.put('/{_id}')
def update_order(
    _id: int,
    order: Order,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_updated = services.update_order(_id, order)

    return order_updated


@router.patch('/{_id}')
def partial_update_order(
    _id: int,
    new_status: OrderPartial,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_updated = services.update_status(_id, new_status)

    return order_updated


@router.delete('/{_id}')
def delete_order(
    _id: int,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    services.delete_order(_id)

    return Response(status_code=status.HTTP_200_OK)


@router.post('/{_id}/items')
def create_order_item(
    _id: int,
    order_item: OrderItemInput,
    order_repository=Depends(order_repository)
):
    services = OrderItemServices(order_repository)

    services.create_item(_id, order_item)

    order_output = services.serializer.serialize_order_output(
        _id).model_dump_json()

    return Response(order_output, status_code=status.HTTP_201_CREATED)


@router.get('/{_id}/items')
def get_order_items(
    _id: int,
    order_repository=Depends(order_repository)
):
    services = OrderItemServices(order_repository)

    order_items = services.get_order_items(_id)

    return order_items


@router.patch('/{order_id}/item/{product_id}')
def update_quantity_order_item(
    order_id: int,
    product_id: int,
    quantity: OrderItemPartial,
    order_repository=Depends(order_repository),
):
    services = OrderItemServices(order_repository)

    order_item = services.update_quantity_order_item(
        order_id, product_id, quantity.quantity
    )

    return order_item


@router.delete('/{order_id}/item/{product_id}')
def delete_order_item(
    order_id: int,
    product_id: int,
    order_repository=Depends(order_repository),
):
    services = OrderItemServices(order_repository)

    order_item = services.delete_order_item(order_id, product_id)

    return order_item
