from app.services.check_services import CheckServices
from app.routes.deps import check_repository, auth
from app.schemas.check import Check, CheckOutput
from fastapi import Depends, Response, status
from fastapi.routing import APIRouter

router = APIRouter(
    prefix='/checks', dependencies=[Depends(auth)], tags=['Checks'])


@router.post(
    '/add', description='Create a check', response_model=CheckOutput)
def create_check(
    check: Check | None,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    if check is None:
        check = Check()

    check_output = services.add_check(check)

    return Response(
        check_output, status_code=status.HTTP_201_CREATED, media_type="json"
    )


@router.get(
    '/{id}', description='List one check', response_model=CheckOutput)
def get_check_by_id(
    id: int,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    check = services.get_check(id)

    return check


@router.get(
    '/', description='List all checks', response_model=list[CheckOutput])
def list_checks(
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    checks = services.get_check()

    return checks


@router.put(
    '/{id}', description='Update a Check', response_model=CheckOutput)
def update_in_use_check(
    id: int,
    check: Check,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    check_updated = services.update_in_use(id, check)

    return check_updated


@router.delete(
    '/{id}', description='Delete a check')
def delete_check(
    id: int,
    check_repository=Depends(check_repository)
):
    services = CheckServices(check_repository)

    services.delete_check(id)

    return Response(status_code=status.HTTP_200_OK)
