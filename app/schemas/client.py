from pydantic import BaseModel, field_validator, PositiveInt
import re


def calculate_cpf(cpf: str) -> str:
    soma = 0
    for index, number in enumerate(cpf, start=1):
        soma += int(number) * index

    first_digit = soma % 11
    first_digit = first_digit if first_digit != 10 else 0

    new_cpf: str = cpf + str(first_digit)

    soma = 0
    for index, number in enumerate(new_cpf):
        soma += int(number) * index

    second_digit = soma % 11
    second_digit = second_digit if second_digit != 10 else 0

    new_cpf = new_cpf + str(second_digit)

    return new_cpf


class Client(BaseModel):
    name: str
    number: str | None
    cpf: str

    @field_validator('number')
    def validate_number(cls, value):
        if value is None:
            return value
        if not re.match(
            "^\([1-9]{2}\) (?:[2-8]|9[0-9])[0-9]{3}\-[0-9]{4}$", value  # noqa
        ):
            raise ValueError('Invalid Number')
        return value

    @field_validator('cpf')
    def validate_cpf(cls, value):
        if value is None:
            return value
        validated_cpf = calculate_cpf(cpf=value[:-2])
        if validated_cpf != value:
            raise ValueError('Invalid CPF')
        return value


class ClientOutput(Client):
    id: PositiveInt
