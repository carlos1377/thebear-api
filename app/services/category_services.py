from app.repositories.sqlalchemy.category_repository import DBCategoryRepository  # noqa
from app.schemas.category import Category, CategoryOutput
from app.db.models import Category as CategoryModel
from fastapi.exceptions import HTTPException
from fastapi import status


class CategoryServices:
    def __init__(self, repository: DBCategoryRepository) -> None:
        self.repository = repository

    def generate_output(self, id: int, client: Category) -> CategoryOutput:
        return CategoryOutput(id=id, **client.model_dump())

    def _if_none_404(self, value, _id: int, model: str = 'Category'):
        if value is None:
            raise HTTPException(
                detail=f'{model} {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

    def add_category(self, category: Category):
        category_model = CategoryModel(**category.model_dump())

        id_category = self.repository.save(category_model)

        return self.generate_output(id_category, category).model_dump_json()

    def list_categories(self, id: int | None = None) -> list | Category | None:
        if id is None:
            categories_on_db = self.repository.get_all()
            return categories_on_db

        category_on_db = self.repository.id_one_or_none(id)
        self._if_none_404(category_on_db, id)

        return category_on_db

    def delete_category(self, id: int) -> None:
        category_on_db = self.repository.id_one_or_none(id)
        self._if_none_404(category_on_db, id)

        self.repository.remove(category_on_db)

        return category_on_db

    def update_category(self, id: int, category: Category):
        category_dump = category.model_dump()

        self._if_none_404(self.repository.id_one_or_none(id), id)

        self.repository.update_object(id, category_dump)

        category_dump['id'] = id

        return CategoryOutput(**category_dump).model_dump_json()
