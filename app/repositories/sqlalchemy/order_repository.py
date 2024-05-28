from app.repositories.sqlalchemy.repository import DBRepository
from app.db.models import OrderItem as OrderItemModel
from app.db.models import Category as CategoryModel
from app.db.models import Product as ProductModel
from app.db.models import Order as OrderModel
from app.db.models import Check as CheckModel
from sqlalchemy.orm import Session


class DBOrderRepository(DBRepository):
    def __init__(self, db_session: Session) -> None:
        self._db_session = db_session
        self._model_service = OrderModel

    def get_order_item_by_ids(self, order_id: int, product_id: int):
        return self._db_session.query(
            OrderItemModel).filter_by(
                order_id=order_id, product_id=product_id).one_or_none()

    def get_check_by_id(self, _id: int):
        return self._db_session.query(CheckModel
                                      ).filter_by(id=_id).one_or_none()

    def get_product_by_id(self, _id: int):
        return self._db_session.query(ProductModel
                                      ).filter_by(id=_id).one_or_none()

    def get_category_by_id(self, _id: int):
        return self._db_session.query(CategoryModel
                                      ).filter_by(id=_id).one_or_none()

    def get_all_order_items_by_order_id(self, order_id: int):
        return self._db_session.query(
            OrderItemModel).filter(OrderItemModel.order_id == order_id).all()

    def remove_all(self, _list):
        for _object in _list:
            self._db_session.delete(_object)
        self._db_session.commit()

    def save(self, _object):
        self._db_session.add(_object)
        self._db_session.commit()
        self._db_session.refresh(_object)

    def save_retrieve_id(self, _object):
        self._db_session.add(_object)
        self._db_session.commit()
        self._db_session.refresh(_object)

        return _object.id
