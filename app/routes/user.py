from app.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository  # noqa
from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import UserServices
from app.db.models import User as UserModel
from app.schemas.user import User, UserLogin
from app.routes.deps import get_db_session
from sqlalchemy.orm import Session

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


@router.post('/login')
def user_login(
    login_request_form: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    repository = SQLAlchemyUserRepository(db_session, UserModel)

    services = UserServices(repository)

    user = UserLogin(
        username=login_request_form.username,
        password=login_request_form.password,
    )

    token_data = services.user_login(user, expires_in=60)

    return token_data
