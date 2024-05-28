from app.repositories.sqlalchemy.product_repository import DBProductRepository
from app.schemas.product import ProductInput, ProductOutput
from app.services.product_services import ProductServices
from fastapi import APIRouter, Depends, Response, status
from app.routes.deps import auth, get_db_session
from sqlalchemy.orm import Session


router = APIRouter(prefix='/products',
                   dependencies=[Depends(auth)], tags=['Products'])


@router.post(
    '/add', description='Create a product', response_model=ProductOutput)
def add_product(
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    product_output = services.add_product(product=product)

    return Response(product_output,
                    status_code=status.HTTP_201_CREATED, media_type="json")


@router.get(
    '/{id}', description='List a product', response_model=ProductOutput)
def list_products_by_id(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    product = services.list_products(id)

    return product


@router.get(
    '/', description='List all products', response_model=list[ProductOutput])
def list_products(
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    products = services.list_products()

    return products


@router.put(
        '/{id}', description='Update a product', response_model=ProductOutput)
def update_product(
    id: int,
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    product_updated = services.update_product(id, product)

    return product_updated


@router.delete(
        '/{id}', description='Delete a product')
def delete_product(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    services.delete_product(id)

    return Response(status_code=status.HTTP_200_OK)
