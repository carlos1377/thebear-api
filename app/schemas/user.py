from pydantic import BaseModel, EmailStr
from pydantic import field_validator, model_validator
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


class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_staff: bool

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[A-Z]|[0-9]|-|_|@)+$', value):
            raise ValueError('Invalid username')
        return value


class TokenData(BaseModel):
    access_token: str
    expires_at: datetime


class FormChangePassword(BaseModel):
    password: str
    confirm_password: str
    new_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'FormChangePassword':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match')
        return self


class FormChangeEmail(BaseModel):
    password: str
    confirm_password: str
    new_email: EmailStr

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'FormChangeEmail':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Passwords do not match')
        return self
