from app.repositories.sqlalchemy.order_repository import SAOrderRepository
from app.schemas.order import Order, OrderPartial
from app.db.models import Order as OrderModel
from fastapi.exceptions import HTTPException
from datetime import datetime
from fastapi import status

# TODO: Quando atribuir um Check a um Order, CHECK.in_use = True
# Posteriormente, quando for finalizar uma comanda, CHECK.in_use = False


class OrderServices:
    def __init__(self, repository: SAOrderRepository) -> None:
        self.repository = repository

    def _format_date(self, date_time):
        return datetime.strftime(date_time, "%Y-%m-%d %X")

    def create_order(self, order: Order):
        check = self.repository.get_check_by_id(order.check_id)

        if check is None:
            raise HTTPException(
                detail=f'Check {order.check_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        order_model = OrderModel(**order.model_dump(mode="json"))
        self.repository.save(order_model)

    def get_order(self, _id: int | None = None):
        if _id is None:
            orders_on_db = self.repository.get_all()

            if len(orders_on_db) > 0:
                for order in orders_on_db:
                    order.date_time = self._format_date(order.date_time)

            return orders_on_db

        order_on_db = self.repository.id_one_or_none(_id)

        if order_on_db is None:
            raise HTTPException(
                detail=f'Order {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        order_on_db.date_time = self._format_date(order_on_db.date_time)

        return order_on_db

    def update_order(self, _id: int, order: Order):
        order_to_update = self.repository.id_one_or_none(_id)

        if order_to_update is None:
            raise HTTPException(
                detail=f'Order {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        self.repository.update_object(
            _id, order.model_dump(mode="json"))

        order_updated = self.repository.id_one_or_none(_id)
        order_updated.date_time = self._format_date(order_updated.date_time)

        return order_updated

    def update_status(self, _id: int, new_status: OrderPartial):
        order_to_update = self.repository.id_one_or_none(_id)

        if order_to_update is None:
            raise HTTPException(
                detail=f'Order {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        self.repository.update_object(
            _id, new_status.model_dump(mode="json"))

        order_updated = self.repository.id_one_or_none(_id)
        order_updated.date_time = self._format_date(order_updated.date_time)

        return order_updated

    def delete_order(self, _id: int):
        order_on_db = self.repository.id_one_or_none(_id)

        if order_on_db is None:
            raise HTTPException(
                detail=f'Order {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )
        self.repository.remove(order_on_db)
