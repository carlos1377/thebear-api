from pydantic import BaseModel, PositiveInt


class Check(BaseModel):
    in_use: bool


class CheckOutput(Check):
    id: PositiveInt
