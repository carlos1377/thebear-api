from app.repositories.sqlalchemy.check_repository import DBCheckRepository
from app.db.models import Check as CheckModel
from fastapi.exceptions import HTTPException
from app.schemas.check import Check, CheckOutput
from fastapi import status


class CheckServices():
    def __init__(self, repository: DBCheckRepository) -> None:
        self.repository = repository

    def add_check(self, check: Check):
        check_model = CheckModel(**check.model_dump())
        self.repository.save(check_model)

    def get_check(
            self, _id: int | None = None) -> CheckOutput | list[CheckOutput]:
        if _id is None:
            checks = self.repository.get_all()

            return checks

        check = self.repository.id_one_or_none(_id)
        if check is None:
            raise HTTPException(
                detail=f'Check {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        return check

    def update_in_use(self, _id: int, check: Check):
        check_to_update = self.repository.id_one_or_none(_id)

        if check_to_update is None:
            raise HTTPException(
                detail=f'Check {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

        self.repository.update_object(_id, check.model_dump())

        check_updated = self.get_check(_id)
        return check_updated

    def delete_check(self, _id: int):
        check = self.get_check(_id)
        self.repository.remove(check)
