from app.schemas.product import Product, ProductInput, ProductOutput
from sqlalchemy.orm import Session
from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from fastapi.exceptions import HTTPException
from fastapi import status


class ProductServices:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    # REFATORAR PARA USAR .query().one_or_none() ao invés da função
    # talvez usar um decorator para testar o output fazer raise HTTPException

    # def none_raises_404(function):
    #     def wrapper(*args, **kwargs):
    #         try:
    #             result = function(*args, **kwargs)
    #         except:
    #
    #         if result is None:
    #             raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f' {slug} not found',
    #         )

    def _find_category_by_slug_or_404(self, slug: str):
        category = self.db_session.query(
            CategoryModel).filter_by(slug=slug).first()

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Category {slug} not found',
            )

        return category

    def add_product(self, product: ProductInput) -> None:
        category = self._find_category_by_slug_or_404(product.category_slug)

        product_model = ProductModel(
            **product.model_dump(exclude={'category_slug'}))
        product_model.category_id = category.id

        self.db_session.add(product_model)
        self.db_session.commit()
        self.db_session.refresh(product_model)

    def list_products(self, _id: int | None = None) -> list[ProductModel] | ProductModel:
        if _id is None:
            products_on_db = self.db_session.query(ProductModel).all()
            return products_on_db
        product_on_db = self.db_session.query(
            ProductModel).filter_by(id=_id).first()

        return product_on_db

    def update_product(self, id: int, product: ProductInput) -> ProductOutput:
        product_on_db = self.db_session.query(
            ProductModel).filter_by(id=id).one_or_none()

        if product_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product {id} not found')

        category = self._find_category_by_slug_or_404(product.category_slug)

        product_on_db.name = product.name
        product_on_db.slug = product.slug
        product_on_db.description = product.description
        product_on_db.price = product.price
        product_on_db.stock = product.stock
        product_on_db.category_id = category.id

        self.db_session.add(product_on_db)
        self.db_session.commit()
        self.db_session.refresh(product_on_db)

        return product_on_db

    def delete_product(self, _id: int) -> None:
        product_on_db = self.db_session.query(
            ProductModel).filter_by(id=_id).one_or_none()

        if product_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Product {_id} not found'
            )
        self.db_session.delete(product_on_db)
        self.db_session.commit()
