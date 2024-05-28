from app.repositories.sqlalchemy.product_repository import DBProductRepository
from app.services.product_services import ProductServices
from fastapi import APIRouter, Depends, Response, status
from app.routes.deps import auth, get_db_session
from app.schemas.product import ProductInput
from sqlalchemy.orm import Session


router = APIRouter(prefix='/products',
                   dependencies=[Depends(auth)], tags=['Products'])


@router.post('/add')
def add_product(
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    product_otp = services.add_product(product=product)

    return Response(product_otp, status_code=status.HTTP_201_CREATED)


@router.get('/{id}')
def list_products_by_id(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    products = services.list_products(id)

    return products


@router.get('/')
def list_products(
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    products = services.list_products()

    return products


@router.put('/{id}')
def update_product(
    id: int,
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    product_updated = services.update_product(id, product)

    return product_updated


@router.delete('/{id}')
def delete_product(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBProductRepository(db_session)
    services = ProductServices(repository)

    services.delete_product(id)

    return Response(status_code=status.HTTP_200_OK)
