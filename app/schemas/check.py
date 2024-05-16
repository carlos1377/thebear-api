from pydantic import BaseModel, PositiveInt


class Check(BaseModel):
    in_use: bool = False


class CheckOutput(Check):
    id: PositiveInt
