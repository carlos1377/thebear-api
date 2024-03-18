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
