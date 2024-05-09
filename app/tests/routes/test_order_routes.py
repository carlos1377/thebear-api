from app.db.models import Order as OrderModel
from app.db.models import OrderItem as OrderItemModel
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app=app)


def test_create_order_route(db_session, check_on_db):
    body = {
        'status': 0,
        'check_id': check_on_db.id
    }

    response = client.post('/order/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    db_session.commit()

    order_on_db = db_session.query(OrderModel).first()

    assert order_on_db is not None
    assert order_on_db.status == body['status']
    assert order_on_db.check_id == body['check_id']

    db_session.delete(order_on_db)
    db_session.commit()


def test_update_order_route(order_on_db):
    body = {
        'status': 2,
        'check_id': order_on_db.check_id
    }

    response = client.put(f'/order/{order_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == {
        'id': order_on_db.id,
        'status': body['status'],
        'check_id': body['check_id'],
        'date_time': str(order_on_db.date_time)
    }


def test_update_order_invalid_id_order_route(order_on_db, check_on_db):
    body = {
        'status': 2,
        'check_id': check_on_db.id
    }

    response = client.put('/order/3', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_order_route(order_on_db):
    response = client.delete(f'/order/{order_on_db.id}')

    assert response.status_code == status.HTTP_200_OK


def test_update_status_order_route(order_on_db):
    body = {
        "status": 1
    }

    response = client.patch(f'/order/{order_on_db.id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['status'] == 1


def test_create_order_item_route(db_session, product_on_db, order_on_db):
    body = {
        'product_id': product_on_db.id,
        'quantity': 1
    }

    response = client.post(f'/order/{order_on_db.id}/items', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    db_session.commit()

    db_session.flush()

    order_item_on_db = db_session.query(OrderItemModel).first()

    assert order_item_on_db is not None

    db_session.delete(order_item_on_db)
    db_session.commit()


def test_get_order_output_route(order_items_on_db):
    order_id = order_items_on_db[0].order_id
    response = client.get(f'/order/{order_id}')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['id'] == order_id
    assert data['order_items'][0]['product']['id'] == order_items_on_db[0].product_id  # noqa
    assert data['order_items'][1]['product']['id'] == order_items_on_db[1].product_id  # noqa


def test_get_order_items_order_route(order_items_on_db):
    order_id = order_items_on_db[0].order_id
    response = client.get(f'/order/{order_id}/items')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[0]['product']['id'] == order_items_on_db[0].product_id
    assert data[1]['quantity'] == order_items_on_db[1].quantity


def test_get_all_orders_route(order_items_on_db):
    response = client.get('/orders/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data[0]['id'] == order_items_on_db[0].order_id
    assert data[0]['order_items'][0]['quantity'] == order_items_on_db[0].quantity  # noqa


def test_update_quantity_order_route(order_item_on_db):
    order_id = order_item_on_db.order_id
    product_id = order_item_on_db.product_id

    body = {
        "quantity": 8
    }

    response = client.patch(f'/order/{order_id}/item/{product_id}', json=body)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data['quantity'] == body['quantity']