from app.schemas.product import ProductOutput
from datetime import datetime
from pydantic import BaseModel, PositiveInt, field_serializer
from enum import Enum


class Status(Enum):
    CONFIRMADO = 0
    EM_PREPARO = 1
    PRONTO = 2
    PAGO = 3


class Order(BaseModel):
    status: Status
    check_id: PositiveInt


class OrderPartial(BaseModel):
    status: Status


class OrderItemPartial(BaseModel):
    quantity: PositiveInt


class OrderItem(BaseModel):
    product: ProductOutput
    quantity: PositiveInt


class OrderOutput(BaseModel):
    id: int
    date_time: datetime
    status: Status
    check_id: PositiveInt | None
    order_items: list[OrderItem]

    @field_serializer('date_time')
    def serialize_date(self, date_time, _info):
        str_date = datetime.strftime(date_time, "%Y-%m-%d %X")
        return str_date


class OrderItemInput(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt
