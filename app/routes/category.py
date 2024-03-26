from fastapi import APIRouter, Depends, Response, status
from app.schemas.category import Category
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.services.category_services import CategoryServices

router = APIRouter(prefix='/category')


@router.post('/add', description='Add new category')
def add_category(
    category: Category, db_session: Session = Depends(get_db_session)
):
    service = CategoryServices(db_session=db_session)

    service.add_category(category=category)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/', description='List all categories')
def list_categories(
    db_session: Session = Depends(get_db_session)
):
    service = CategoryServices(db_session=db_session)

    categories = service.list_categories()

    return categories


@router.get('/{id}', description='List one category')
def list_categories_by_id(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    service = CategoryServices(db_session=db_session)

    category = service.list_categories(id=id)

    return category


@router.delete('/{id}', description='Delete a category')
def delete_category(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    service = CategoryServices(db_session)

    service.delete_category(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.put('/{id}', description='Update a category')
def update_category(
    category: Category,
    id: int,
    db_session: Session = Depends(get_db_session)
):
    service = CategoryServices(db_session)

    service.update_category(id=id, category=category)

    return Response(status_code=status.HTTP_200_OK)
