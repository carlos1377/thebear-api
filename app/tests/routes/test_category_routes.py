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


def test_list_categories_route(categories_on_db):
    response = client.get('/category')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 4
    assert data[0] == {
        "name": categories_on_db[0].name,
        "slug": categories_on_db[0].slug,
        "id": categories_on_db[0].id,
    }


def test_list_categories_by_id_route(categories_on_db):
    response = client.get(f'/category/{categories_on_db[2].id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "name": categories_on_db[2].name,
        "slug": categories_on_db[2].slug,
        "id": categories_on_db[2].id,
    }


def test_delete_category_route(db_session):
    category_model = CategoryModel(name='Roupa', slug='roupa')

    db_session.add(category_model)
    db_session.commit()

    response = client.delete(f'/category/{category_model.id}')

    assert response.status_code == status.HTTP_200_OK


def test_delete_category_route_invalid_id():
    response = client.delete('/category/-40')

    assert response.status_code == status.HTTP_404_NOT_FOUND
