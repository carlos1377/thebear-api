from app.schemas.category import Category
from sqlalchemy.orm import Session
from app.db.models import Category as CategoryModel
from fastapi.exceptions import HTTPException
from fastapi import status


class CategoryServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def find_by_id_or_404(self, id: int) -> Category | None:
        category = self.db_session.query(
            CategoryModel).filter_by(id=id).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category {id} not found',
            )

        return category

    def add_category(self, category: Category) -> None:
        category_model = CategoryModel(**category.model_dump())

        self.db_session.add(category_model)
        self.db_session.commit()

    def list_categories(self, id: int | None = None) -> list | Category:
        if id is None:
            categories_on_db = self.db_session.query(CategoryModel).all()
            return categories_on_db

        category_on_db = self.find_by_id_or_404(id)
        return category_on_db

    def delete_category(self, id: int):
        category_on_db = self.find_by_id_or_404(id)

        self.db_session.delete(category_on_db)
        self.db_session.commit()
