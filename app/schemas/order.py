from pydantic import BaseModel


class Order(BaseModel):
    status: str
    mesa: int


class OrderOutput(Order):
    id: int
