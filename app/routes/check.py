from app.services.check_services import CheckServices
from app.routes.deps import check_repository
from fastapi.routing import APIRouter
from app.schemas.check import Check
from fastapi import Depends, Response, status

router = APIRouter(prefix='/check')


@router.post('/add')
def create_check(
    check: Check,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    services.add_check(check)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/{_id}')
def get_check_by_id(
    _id: int,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    check = services.get_check(_id)

    return check


@router.get('/')
def list_checks(
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    checks = services.get_check()

    return checks


@router.put('/{_id}')
def update_in_use_check(
    _id: int,
    check: Check,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    check_updated = services.update_in_use(_id, check)

    return check_updated


@router.delete('/{_id}')
def delete_check(
    _id: int,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    services.delete_check(_id)

    return Response(status_code=status.HTTP_200_OK)