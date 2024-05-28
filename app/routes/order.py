from app.services.order_services import OrderServices, OrderItemServices
from app.schemas.order import (
    Order, OrderPartial, OrderItemInput, OrderItemPartial, OrderOutput,
    OrderItem
)
from app.routes.deps import order_repository, auth
from fastapi import Depends, Response, status
from fastapi.routing import APIRouter

router = APIRouter(prefix='/orders',
                   dependencies=[Depends(auth)], tags=['Orders'])


@router.post(
    '/add', description='Create a order', response_model=OrderOutput)
def create_order(
    order: Order,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_output = services.create_order(order)

    return Response(order_output.model_dump_json(),
                    status_code=status.HTTP_201_CREATED, media_type="json")


@router.get(
    '/{id}', description='List a order', response_model=OrderOutput)
def get_order_output(
    id: int,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_output = services.serializer.serialize_order_output(id)

    return order_output


@router.get(
    '/', description='List all orders', response_model=list[OrderOutput])
def get_all_orders(
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    orders = services.get_all_orders()

    return orders


@router.put(
    '/{id}', description='Update a order', response_model=OrderOutput)
def update_order(
    id: int,
    order: Order,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_updated = services.update_order(id, order)

    return order_updated


@router.patch(
    '/{id}', description='Partial update a order', response_model=OrderOutput)
def partial_update_order(
    id: int,
    new_status: OrderPartial,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    order_updated = services.update_status(id, new_status)

    return order_updated


@router.delete('/{id}', description='Delete a order')
def delete_order(
    id: int,
    order_repository=Depends(order_repository)
):
    services = OrderServices(order_repository)

    services.delete_order(id)

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    '/{id}/items', description='Create a order item',
    response_model=OrderOutput)
def create_order_item(
    id: int,
    order_item: OrderItemInput,
    order_repository=Depends(order_repository)
):
    services = OrderItemServices(order_repository)

    services.create_item(id, order_item)

    order_output = services.serializer.serialize_order_output(
        id)

    return Response(order_output.model_dump_json(),
                    status_code=status.HTTP_201_CREATED, media_type="json")


@router.get(
    '/{id}/items', description='List all order item',
    response_model=list[OrderItem])
def get_order_items(
    id: int,
    order_repository=Depends(order_repository)
):
    services = OrderItemServices(order_repository)

    order_items = services.get_order_items(id)

    return order_items


@router.patch(
    '/{order_id}/items/{product_id}',
    description='Update quantity on a order item', response_model=OrderItem)
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


@router.delete(
    '/{order_id}/items/{product_id}',
    description='Delete a order item')
def delete_order_item(
    order_id: int,
    product_id: int,
    order_repository=Depends(order_repository),
):
    services = OrderItemServices(order_repository)

    order_item = services.delete_order_item(order_id, product_id)

    return order_item
