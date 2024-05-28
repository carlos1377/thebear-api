from app.db.models import Product as ProductModel
from app.db.models import Category as CategoryModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app=app)

header = {'Authorization': 'Bearer token'}

client.headers = header  # type: ignore


def test_add_product_route(db_session):
    category_on_db = CategoryModel(name='foo', slug='bar')

    db_session.add(category_on_db)
    db_session.commit()
    db_session.refresh(category_on_db)

    category_id = category_on_db.id

    body = {
        "name": "Heineken",
        "slug": "bebida-heineken",
        "price": 16.6,
        "stock": 20,
        "description": None,
        "category_slug": 'bar',
    }

    response = client.post('/products/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    product_on_db = db_session.query(ProductModel).first()

    data = response.json()

    db_session.flush()

    category_on_db = db_session.query(CategoryModel).first()

    db_session.delete(category_on_db)
    db_session.commit()

    product_on_db = db_session.query(ProductModel).first()

    assert data == {
        "id": product_on_db.id,
        "name": body["name"],
        "slug": body["slug"],
        "price": body["price"],
        "stock": body["stock"],
        "description": body["description"],
        "category": {
            "id": category_id,
            "name": category_on_db.name,
            "slug": category_on_db.slug
        }
    }

    assert product_on_db is not None
    assert product_on_db.category_id is None
    assert product_on_db.name == 'Heineken'

    db_session.delete(product_on_db)
    db_session.commit()


def test_list_product_route(db_session, product_on_db, category_on_db):
    response = client.get('/products/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[0] == {
        "id": product_on_db.id,
        "name": product_on_db.name,
        "slug": product_on_db.slug,
        "price": product_on_db.price,
        "stock": product_on_db.stock,
        "description": product_on_db.description,
        "category": {
            "id": category_on_db.id,
            "name": category_on_db.name,
            "slug": category_on_db.slug
        }
    }


def test_list_product_by_id_route(db_session, product_on_db, category_on_db):
    _id = product_on_db.id

    response = client.get(f'/products/{_id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "id": product_on_db.id,
        "name": product_on_db.name,
        "slug": product_on_db.slug,
        "price": product_on_db.price,
        "stock": product_on_db.stock,
        "description": product_on_db.description,
        "category": {
            "id": category_on_db.id,
            "name": category_on_db.name,
            "slug": category_on_db.slug
        }
    }


def test_update_product_route(product_on_db, category_on_db):
    id = product_on_db.id

    body = {
        "name": 'Rock Stone',
        "slug": 'rock-stone',
        "price": 14.99,
        "stock": 5,
        "description": None,
        "category_slug": category_on_db.slug
    }

    response = client.put(f'/products/{id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "id": id,
        "name": body['name'],
        "slug": body['slug'],
        "price": body['price'],
        "stock": body['stock'],
        "description": body['description'],
        "category": {
            "id": category_on_db.id,
            "name": category_on_db.name,
            "slug": category_on_db.slug
        }
    }


def test_delete_product_route(product_on_db):
    _id = product_on_db.id

    response = client.delete(f'/products/{_id}')

    assert response.status_code == status.HTTP_200_OK


def test_delete_product_invalid_id_route():
    _id = -66

    response = client.delete(f'/products/{_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND
