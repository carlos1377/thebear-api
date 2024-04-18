from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.routes.deps import auth, get_db_session
from app.schemas.product import ProductInput
from app.services.product_services import ProductServices


router = APIRouter(prefix='/product',  dependencies=[Depends(auth)])


@router.post('/add')
def add_product(
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    services.add_product(product=product)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/{_id}')
def list_products_by_id(
    _id: int,
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    products = services.list_products(_id)

    return products


@router.get('/')
def list_products(
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    products = services.list_products()

    return products


@router.put('/{id}')
def update_product(
    id: int,
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    product_updated = services.update_product(id, product)

    return product_updated


@router.delete('/{_id}')
def delete_product(
    _id: int,
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    services.delete_product(_id)

    return Response(status_code=status.HTTP_200_OK)
