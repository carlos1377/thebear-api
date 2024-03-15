from pydantic import BaseModel, PositiveInt


class OrderItem(BaseModel):
    product_id: PositiveInt
    order_id: PositiveInt
    quantity: PositiveInt
