from app.schemas.check import Check, CheckOutput
import pytest


def test_check_schema():
    check = Check(in_use=True)

    assert check.model_dump() == {
        'in_use': True
    }


def test_check_schema_invalid_in_use():
    with pytest.raises(ValueError):
        check = Check(in_use=None)


def test_check_output_schema():
    check = CheckOutput(in_use=True, id=4)

    assert check.model_dump() == {
        'id': 4,
        'in_use': True
    }


def test_check_output_schema_invalid_id():
    with pytest.raises(ValueError):
        check = CheckOutput(in_use=True, id=-7)
