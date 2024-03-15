from app.schemas.category import Category
from sqlalchemy.orm import Session
from app.db.models import Category as CategoryModel


class CategoryServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def add_category(self, category: Category) -> None:
        category_model = CategoryModel(**category.model_dump())

        self.db_session.add(category_model)
        self.db_session.commit()
