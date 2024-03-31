from app.db.models import Product as ProductModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app=app)


def test_add_product_route(db_session, category_on_db):
    body = {
        "name": "Heineken",
        "slug": "bebida-heineken",
        "price": 16.6,
        "stock": 20,
        "description": None,
        "category_slug": category_on_db.slug,
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    db_session.flush()

    product_on_db = db_session.query(ProductModel).all()

    assert len(product_on_db) == 1

    db_session.delete(product_on_db[0])
    db_session.commit()
