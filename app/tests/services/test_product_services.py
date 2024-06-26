from app.repositories.sqlalchemy.product_repository import DBProductRepository
from app.schemas.product import ProductInput
from app.db.models import Product as ProductModel
from app.services.product_services import ProductServices


def test_add_product_service(db_session, category_on_db):
    product = ProductInput(
        name='Heineken', slug='heineken', price=12.49, stock=50,
        description='uma boa cerveja!', category_slug=category_on_db.slug
    )

    repository = DBProductRepository(db_session)
    service = ProductServices(repository)

    service.add_product(product)

    product_on_db = db_session.query(ProductModel).first()

    assert product_on_db is not None

    assert product_on_db.name == 'Heineken'
    assert product_on_db.slug == 'heineken'
    assert product_on_db.price == 12.49
    assert product_on_db.stock == 50
    assert product_on_db.description == 'uma boa cerveja!'
    assert product_on_db.category.name == category_on_db.name
    assert product_on_db.category.slug == category_on_db.slug

    db_session.delete(product_on_db)
    db_session.commit()


def test_list_product_services(db_session, product_on_db):
    repository = DBProductRepository(db_session)
    service = ProductServices(repository)

    product = service.list_products()

    assert len(product) == 1
    assert product[0].name == product_on_db.name
    assert product[0].stock == product_on_db.stock


def test_list_product_by_id_services(db_session, product_on_db):
    _id = product_on_db.id

    repository = DBProductRepository(db_session)
    service = ProductServices(repository)

    product = service.list_products(_id)

    assert product is not None
    assert product.name == product_on_db.name
    assert product.stock == product_on_db.stock


def test_update_product_services(db_session, product_on_db, category_on_db):
    new_product = ProductInput(
        name='Polar', slug='polar', price=7.55, stock=240,
        description='polar dos guri', category_slug=category_on_db.slug
    )

    repository = DBProductRepository(db_session)
    service = ProductServices(repository)

    service.update_product(product_on_db.id, new_product)

    product_on_db = db_session.query(ProductModel).first()

    assert product_on_db is not None
    assert product_on_db.name == new_product.name
    assert product_on_db.slug == new_product.slug
    assert product_on_db.price == new_product.price


def test_delete_product_services(db_session, product_on_db):
    repository = DBProductRepository(db_session)
    service = ProductServices(repository)

    service.delete_product(product_on_db.id)

    query_product = db_session.query(ProductModel).filter_by(
        id=product_on_db.id).one_or_none()

    assert query_product is None
