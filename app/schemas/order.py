from app.schemas.check import CheckOutput
from datetime import datetime
from pydantic import BaseModel, PositiveInt
from enum import Enum


class Status(Enum):
    CONFIRMADO = 0
    EM_PREPARO = 1
    PRONTO = 2
    PAGO = 3


class Order(BaseModel):
    status: Status
    check_id: PositiveInt


class OrderOutput(BaseModel):
    id: int
    date_time: datetime
    status: Status
    check: CheckOutput
