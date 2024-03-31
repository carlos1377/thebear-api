from app.schemas.product import Product
from sqlalchemy.orm import Session
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from fastapi.exceptions import HTTPException
from fastapi import status


class ProductServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def _find_category_by_slug_or_404(self, slug: str):
        category = self.db_session.query(
            CategoryModel).filter_by(slug=slug).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category {slug} not found',
            )

        return category

    def add_product(self, product: Product, category_slug: str) -> None:
        category = self._find_category_by_slug_or_404(category_slug)

        product_model = ProductModel(**product.model_dump())
        product_model.category_id = category.id

        self.db_session.add(product_model)
        self.db_session.commit()
