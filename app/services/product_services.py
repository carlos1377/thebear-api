from app.repositories.sqlalchemy.product_repository import DBProductRepository
from app.schemas.product import ProductInput, ProductOutput
from app.schemas.category import CategoryOutput
from app.db.models import Product as ProductModel
from fastapi.exceptions import HTTPException
from fastapi import status


class ProductServices:
    def __init__(self, repository: DBProductRepository) -> None:
        self.repository = repository

    def serialize_category(self, category) -> CategoryOutput:
        return CategoryOutput(
            id=category.id, name=category.name, slug=category.slug
        )

    def generate_output(
        self, id: int, product: ProductInput, category: CategoryOutput
    ):
        return ProductOutput(
            id=id, **product.model_dump(exclude={'category_slug'}),
            category=category
        ).model_dump_json()

    def _if_none_404(self, value, _id: int, model: str = 'Product'):
        if value is None:
            raise HTTPException(
                detail=f'{model} {_id} not found',
                status_code=status.HTTP_404_NOT_FOUND
            )

    def add_product(self, product: ProductInput):
        category = self.repository._find_category_by_slug(
            product.category_slug)
        self._if_none_404(category, category.id)

        product_model = ProductModel(
            **product.model_dump(exclude={'category_slug'}),
            category_id=category.id)

        id = self.repository.save(product_model)

        category = self.serialize_category(category)

        return self.generate_output(id, product, category)

    def list_products(self, _id: int | None = None) -> list | ProductModel:
        if _id is None:
            products_on_db = self.repository.get_all()
            return products_on_db

        product_on_db = self.repository.id_one_or_none(_id)
        self._if_none_404(product_on_db, _id)

        return product_on_db

    def update_product(self, _id: int, product: ProductInput):
        product_on_db = self.repository.id_one_or_none(_id)
        self._if_none_404(product_on_db, _id)

        product_dump = product.model_dump()

        category = self.repository._find_category_by_slug(
            product.category_slug)

        self.repository.update_object(_id, product_dump)

        product_output = ProductOutput(
            **product.model_dump(exclude={'category_slug'}),
            id=product_on_db.id, category=category
        )
        return product_output

    def delete_product(self, _id: int) -> None:
        product_on_db = self.repository.id_one_or_none(_id)
        self._if_none_404(product_on_db, _id)

        self.repository.remove(product_on_db)
