from pydantic import BaseModel, field_validator, ConfigDict
import re


class Category(BaseModel):
    name: str
    slug: str

    @field_validator('slug')
    def validate_slug(cls, value):
        if not re.match('^([a-z]|[0-9]|-|_)+$', value):
            raise ValueError('Invalid slug')
        return value


class CategoryOutput(Category):
    model_config = ConfigDict(from_attributes=True)

    id: int
