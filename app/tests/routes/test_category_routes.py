from app.db.models import Category as CategoryModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app=app)

header = {'Authorization': 'Bearer token'}

client.headers = header  # type: ignore


def test_add_category_route(db_session):
    body = {
        "name": "Bebida",
        "slug": "bebida"
    }

    response = client.post('/categories/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    category_on_db = db_session.query(CategoryModel).all()

    assert len(category_on_db) == 1

    assert data == {
        'id': category_on_db[0].id,
        'name': body['name'],
        'slug': body['slug'],
    }

    db_session.delete(category_on_db[0])
    db_session.commit()


def test_list_categories_route(categories_on_db):
    response = client.get('/categories')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 4
    assert data[0] == {
        "name": categories_on_db[0].name,
        "slug": categories_on_db[0].slug,
        "id": categories_on_db[0].id,
    }


def test_list_categories_by_id_route(categories_on_db):
    response = client.get(f'/categories/{categories_on_db[2].id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        "name": categories_on_db[2].name,
        "slug": categories_on_db[2].slug,
        "id": categories_on_db[2].id,
    }


def test_list_categories_by_id_route_invalid_id():
    response = client.get('/categories/3')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category_route(db_session):
    category_model = CategoryModel(name='Roupa', slug='roupa')

    db_session.add(category_model)
    db_session.commit()

    response = client.delete(f'/categories/{category_model.id}')

    assert response.status_code == status.HTTP_200_OK


def test_delete_category_route_invalid_id():
    response = client.delete('/categories/-40')

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_category_route(db_session, category_on_db):
    id = category_on_db.id

    body = {
        "name": "Foo",
        "slug": "bar"
    }

    response = client.put(
        f'/categories/{id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    db_session.refresh(category_on_db)

    updated_category_on_db = db_session.query(CategoryModel) \
        .filter_by(id=id).first()

    data = response.json()

    assert data == {
        'id': id,
        'name': body['name'],
        'slug': body['slug']
    }

    assert updated_category_on_db is not None
    assert updated_category_on_db.name == 'Foo'
    assert updated_category_on_db.slug == 'bar'
