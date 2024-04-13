from pydantic import BaseModel, EmailStr, field_validator
import re


class Client(BaseModel):
    name: str
    email: EmailStr
    number: str | None
    password: str

    @field_validator('number')
    def validate_number(cls, value):
        if value is None:
            return value
        if not re.match(
            "^\([1-9]{2}\) (?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$", value  # noqa
        ):
            raise ValueError('Invalid Number')
        return value
