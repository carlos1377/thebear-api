from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.product import ProductInput
from app.services.product_services import ProductServices


router = APIRouter(prefix='/product')


@router.post('/add')
def add_product(
    product: ProductInput,
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    services.add_product(product=product)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/')
def list_products(
    db_session: Session = Depends(get_db_session)
):
    services = ProductServices(db_session=db_session)

    products = services.list_products()

    return products
