from app.repositories.sqlalchemy.order_repository import SAOrderRepository
from app.schemas.order import Order
from app.db.models import Order as OrderModel
from fastapi.exceptions import HTTPException
from fastapi import status


class OrderServices:
    def __init__(self, repository: SAOrderRepository) -> None:
        self.repository = repository

    def create_order(self, order: Order):
        order_model = OrderModel(**order.model_dump(mode="json"))
        self.repository.save(order_model)

    def get_order(self, _id: int):
        order_on_db = self.repository.id_one_or_none(_id)

        if order_on_db is None:
            raise HTTPException(
                detail='Order {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return order_on_db
