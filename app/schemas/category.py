from pydantic import BaseModel, field_validator
import re


class Category(BaseModel):
    name: str
    slug: str

    @field_validator('slug')
    def validate_slug(cls, value):
        if not re.match('^([a-z]|[0-9]|-|_)+$', value):
            raise ValueError('Invalid slug')
        return value
