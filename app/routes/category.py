from app.repositories.sqlalchemy.category_repository import DBCategoryRepository  # noqa
from app.services.category_services import CategoryServices
from app.schemas.category import Category, CategoryOutput
from fastapi import APIRouter, Depends, Response, status
from app.routes.deps import auth, get_db_session
from sqlalchemy.orm import Session


router = APIRouter(prefix='/categories',
                   dependencies=[Depends(auth)], tags=['Categories'])


@router.post(
    '/add', description='Create a category', response_model=CategoryOutput)
def add_category(
    category: Category, db_session: Session = Depends(get_db_session)
):
    repository = DBCategoryRepository(db_session)
    service = CategoryServices(repository)

    category_otp = service.add_category(category=category)

    return Response(
        category_otp, status_code=status.HTTP_201_CREATED, media_type="json"
    )


@router.get(
    '/', description='List all categories',
    response_model=list[CategoryOutput])
def list_categories(
    db_session: Session = Depends(get_db_session)
):
    repository = DBCategoryRepository(db_session)
    service = CategoryServices(repository)

    categories = service.list_categories()

    return categories


@router.get(
    '/{id}', description='List one category', response_model=CategoryOutput)
def list_categories_by_id(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBCategoryRepository(db_session)
    service = CategoryServices(repository)

    category = service.list_categories(id=id)

    return category


@router.delete('/{id}', description='Delete a category')
def delete_category(
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBCategoryRepository(db_session)
    service = CategoryServices(repository)

    service.delete_category(id=id)

    return Response(status_code=status.HTTP_200_OK)


@router.put(
    '/{id}', description='Update a category',
    response_model=CategoryOutput)
def update_category(
    category: Category,
    id: int,
    db_session: Session = Depends(get_db_session)
):
    repository = DBCategoryRepository(db_session)
    service = CategoryServices(repository)

    categoty_otp = service.update_category(id=id, category=category)

    return Response(categoty_otp,
                    status_code=status.HTTP_200_OK, media_type="json")
