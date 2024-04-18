from pydantic import BaseModel, EmailStr
from pydantic import field_validator
from datetime import datetime
import re


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_staff: bool

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Invalid username')
        return value


class UserLogin(BaseModel):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Invalid username')
        return value


class TokenData(BaseModel):
    access_token: str
    expires_at: datetime
