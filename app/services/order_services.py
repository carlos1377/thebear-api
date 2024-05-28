from app.repositories.sqlalchemy.order_repository import DBOrderRepository
from app.schemas.order import (
    Order, OrderPartial, OrderItemInput, OrderOutput, OrderItem
)
from app.db.models import OrderItem as OrderItemModel
from app.db.models import Order as OrderModel
from app.schemas.product import ProductOutput
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi import status

# TODO: Quando atribuir um Check a um Order, CHECK.in_use = True
# Posteriormente, quando for finalizar uma comanda, CHECK.in_use = False
# TODO: METHOD orders/{id}/items/


def format_date(date_time):
    return datetime.strftime(date_time, "%Y-%m-%d %X")


class OrdersSerializers:
    def __init__(self, repository: DBOrderRepository) -> None:
        self.repository = repository

    def _serialize_order_item(self, order_item_in: OrderItemInput) -> OrderItem:  # noqa
        product = jsonable_encoder(
            self.repository.get_product_by_id(order_item_in.product_id))
        category = jsonable_encoder(
            self.repository.get_category_by_id(product['category_id']))

        order_item_schema = OrderItem(
            product=ProductOutput(**product, category=category),
            quantity=order_item_in.quantity
        )

        return order_item_schema

    def serialize_order_output(self, order_id: int):
        order = self.repository.id_one_or_none(order_id)

        order = jsonable_encoder(order)
        order_items = self.repository.get_all_order_items_by_order_id(order_id)

        serialized_orders_items = [
            self._serialize_order_item(OrderItemInput(
                product_id=order_item.product_id, quantity=order_item.quantity)
            ) for order_item in order_items
        ]

        order_output = OrderOutput(
            **order, order_items=jsonable_encoder(serialized_orders_items))

        return order_output


class OrderServices:
    def __init__(self, repository: DBOrderRepository) -> None:
        self.repository = repository
        self.serializer = OrdersSerializers(repository)

    def _if_none_404(self, value, _id: int, model: str = 'Order'):
        if value is None:
            raise HTTPException(
                detail=f'{model} {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

    def get_all_orders(self):
        orders = self.repository.get_all()

        serialized_orders = [
            self.serializer.serialize_order_output(order.id)
            for order in orders
        ]

        return serialized_orders

    def create_order(self, order: Order):
        self._if_none_404(
            self.repository.get_check_by_id(order.check_id), order.check_id,
            model='Check'
        )

        order_model = OrderModel(**order.model_dump(mode="json"))
        order_id = self.repository.save_retrieve_id(order_model)

        return self.serializer.serialize_order_output(order_id)

    def update_order(self, _id: int, order: Order):
        self._if_none_404(self.repository.id_one_or_none(_id), _id)

        self.repository.update_object(
            _id, order.model_dump(mode="json"))

        order_updated = self.repository.id_one_or_none(_id)
        order_updated.date_time = format_date(order_updated.date_time)

        return self.serializer.serialize_order_output(_id)

    def update_status(self, _id: int, new_status: OrderPartial):
        self._if_none_404(self.repository.id_one_or_none(_id), _id)

        self.repository.update_object(
            _id, new_status.model_dump(mode="json"))

        order_updated = self.repository.id_one_or_none(_id)
        order_updated.date_time = format_date(order_updated.date_time)

        return self.serializer.serialize_order_output(_id)

    def delete_order(self, _id: int):
        order_on_db = self.repository.id_one_or_none(_id)
        self._if_none_404(order_on_db, _id)

        self.repository.remove(order_on_db)


class OrderItemServices:
    def __init__(self, repository: DBOrderRepository) -> None:
        self.repository = repository
        self.serializer = OrdersSerializers(repository)

    def _if_none_404(self, value, _id: int, model: str = 'Order'):
        if value is None:
            raise HTTPException(
                detail=f'{model} {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

    def create_item(self, id_order: int, order_item: OrderItemInput):
        self._if_none_404(self.repository.id_one_or_none(id_order), id_order)
        self._if_none_404(
            self.repository.get_product_by_id(order_item.product_id),
            order_item.product_id, model='Product'
        )

        order_item_model = OrderItemModel(
            order_id=id_order, **order_item.model_dump()
        )

        self.repository.save(order_item_model)

    def get_order_items(self, id_order: int):
        self._if_none_404(self.repository.id_one_or_none(id_order), id_order)

        order_items = self.repository.get_all_order_items_by_order_id(id_order)

        serialized_orders_items = [
            self.serializer._serialize_order_item(OrderItemInput(
                product_id=order_item.product_id, quantity=order_item.quantity)
            ) for order_item in order_items
        ]
        return serialized_orders_items

    def update_quantity_order_item(
            self, id_order: int, id_product: int, quantity: int):

        self._if_none_404(
            self.repository.id_one_or_none(id_order), id_order)
        self._if_none_404(
            self.repository.get_product_by_id(id_product),
            id_product, 'Product')

        order_item = self.repository.get_order_item_by_ids(
            id_order, id_product)

        order_item.quantity = quantity

        self.repository.save(order_item)

        return self.serializer._serialize_order_item(
            OrderItemInput(product_id=id_product, quantity=quantity)
        )

    def delete_order_item(self, id_order: int, id_product: int):
        self._if_none_404(
            self.repository.id_one_or_none(id_order), id_order)
        self._if_none_404(
            self.repository.get_product_by_id(id_product),
            id_product, 'Product')

        order_item = self.repository.get_order_item_by_ids(
            id_order, id_product)

        self.repository.remove(order_item)

        return self.serializer._serialize_order_item(
            OrderItemInput(product_id=id_product, quantity=order_item.quantity)
        )
