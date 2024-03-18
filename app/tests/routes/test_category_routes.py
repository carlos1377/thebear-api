from fastapi.testclient import TestClient
from app.main import app
from app.db.models import Category as CategoryModel
from fastapi import status
client = TestClient(app=app)


def test_add_category_route(db_session):
    body = {
        "name": "Bebida",
        "slug": "bebida"
    }

    response = client.post('/category/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    category_on_db = db_session.query(CategoryModel).all()

    assert len(category_on_db) == 1

    db_session.delete(category_on_db[0])
    db_session.commit()
