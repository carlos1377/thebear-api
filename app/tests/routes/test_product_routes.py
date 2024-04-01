from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app=app)


def test_add_product_route(db_session):
    category_on_db = CategoryModel(name='foo', slug='bar')

    db_session.add(category_on_db)
    db_session.commit()
    db_session.refresh(category_on_db)

    body = {
        "name": "Heineken",
        "slug": "bebida-heineken",
        "price": 16.6,
        "stock": 20,
        "description": None,
        "category_slug": 'bar',
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    db_session.flush()

    category_on_db = db_session.query(CategoryModel).first()

    db_session.delete(category_on_db)
    db_session.commit()

    product_on_db = db_session.query(ProductModel).first()

    assert product_on_db.category_id is None
    assert product_on_db.name == 'Heineken'

    db_session.delete(product_on_db)
    db_session.commit()
