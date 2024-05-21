from app.repositories.sqlalchemy.check_repository import DBCheckRepository
from app.services.check_services import CheckServices
from fastapi.exceptions import HTTPException
from app.schemas.check import Check
import pytest


def test_check_add_services(db_session):
    repository = DBCheckRepository(db_session)
    services = CheckServices(repository)

    check = Check(in_use=False)

    services.add_check(check)

    check_on_db = services.repository.find_first()

    assert check_on_db is not None

    services.repository.remove(check_on_db)


def test_check_get_services(db_session, check_on_db):
    repository = DBCheckRepository(db_session)
    services = CheckServices(repository)

    check = services.get_check(check_on_db.id)

    assert check is not None

    assert check.id == check_on_db.id
    assert check.in_use == check_on_db.in_use


def test_check_list_all_services(db_session, checks_on_db):
    repository = DBCheckRepository(db_session)
    services = CheckServices(repository)

    checks = services.get_check()

    assert len(checks) > 0

    assert checks[1].id == checks_on_db[1].id
    assert checks[1].in_use == checks_on_db[1].in_use


def test_check_update_services(db_session, check_on_db):
    repository = DBCheckRepository(db_session)
    services = CheckServices(repository)

    check = Check(in_use=True)

    check_updated = services.update_in_use(check_on_db.id, check)

    assert check_updated is not None

    assert check_updated.id == check_on_db.id
    assert check_updated.in_use is True


def test_check_delete_services(db_session, checks_on_db):
    repository = DBCheckRepository(db_session)
    services = CheckServices(repository)

    services.delete_check(checks_on_db[0].id)

    with pytest.raises(HTTPException):
        services.get_check(checks_on_db[0].id)
