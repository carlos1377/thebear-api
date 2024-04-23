from pydantic import BaseModel
from enum import Enum


class Status(Enum):
    CONFIRMADO = 0
    EM_PREPARO = 1
    PRONTO = 2
    PAGO = 3


class Order(BaseModel):
    status: Status
    mesa: int


class OrderOutput(Order):
    id: int
