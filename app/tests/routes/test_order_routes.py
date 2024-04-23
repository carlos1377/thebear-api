from app.db.models import Order as OrderModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app=app)


def test_create_order_route(db_session):
    body = {
        'status': 0,
        'mesa': 5
    }

    response = client.post('/order/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    order_on_db = db_session.query(OrderModel).first()

    assert order_on_db is not None
    assert order_on_db.status == body['status']
    assert order_on_db.mesa == body['mesa']

    db_session.delete(order_on_db)
    db_session.commit()


def test_get_by_id_order_route(order_on_db):
    response = client.get(f'/order/{order_on_db.id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': order_on_db.id,
        'status': order_on_db.status,
        'mesa': order_on_db.mesa,
        'date_time': str(order_on_db.date_time)
    }


def test_list_orders_order_route(orders_on_db):
    response = client.get('order/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[1] == {
        'id': orders_on_db[1].id,
        'status': orders_on_db[1].status,
        'mesa': orders_on_db[1].mesa,
        'date_time': str(orders_on_db[1].date_time)
    }

    assert data[2] == {
        'id': orders_on_db[2].id,
        'status': orders_on_db[2].status,
        'mesa': orders_on_db[2].mesa,
        'date_time': str(orders_on_db[2].date_time)
    }


def test_update_order_route(order_on_db):
    body = {
        'status': 2,
        'mesa': 7
    }

    response = client.put(f'/order/{order_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': order_on_db.id,
        'status': body['status'],
        'mesa': body['mesa'],
        'date_time': str(order_on_db.date_time)
    }


def test_update_order_invalid_id_order_route(order_on_db):
    body = {
        'status': 2,
        'mesa': 7
    }

    response = client.put('/order/3', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_order_route(order_on_db):
    response = client.delete(f'/order/{order_on_db.id}')

    assert response.status_code == status.HTTP_200_OK
