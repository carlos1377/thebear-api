from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.routes.deps import get_db_session
from app.schemas.client import Client
from app.services.client_services import ClientServices

router = APIRouter(prefix='/client')


@router.post('/add')
def add_product(
    client: Client,
    db_session: Session = Depends(get_db_session),
):
    services = ClientServices(db_session=db_session)

    services.add_client(client=client)

    return Response(status_code=status.HTTP_201_CREATED)
