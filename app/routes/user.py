from fastapi import APIRouter, Response, status, Depends
from app.db.models import User as UserModel
from app.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository  # noqa
from app.schemas.user import User, TokenData
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.services.user_services import UserServices


router = APIRouter(prefix='/user')


@router.post('/register')
def user_register(
    user: User,
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyUserRepository(db_session, UserModel)

    services = UserServices(repository)

    services.register_user(user)

    return Response(status_code=status.HTTP_201_CREATED)
