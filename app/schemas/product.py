from pydantic import BaseModel, field_validator
from app.schemas.category import Category
import re


class Product(BaseModel):
    name: str
    slug: str
    price: float
    description: str | None
    stock: int

    @field_validator('price')
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError('Invalid price value')
        return value

    @field_validator('slug')
    def validate_slug(cls, value):
        if not re.match('^([a-z]|[0-9]|-|_)+$', value):
            raise ValueError('Invalid slug')
        return value


class ProductOutput(Product):
    id: int
    category: Category


class ProductInput(Product):
    category_slug: str
