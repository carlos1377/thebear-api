from app.schemas.product import Product, ProductInput
from app.db.models import Product as ProductModel
from app.services.product_services import ProductServices
from app.schemas.category import Category


def test_add_product_service(db_session, category_on_db):
    product = ProductInput(
        name='Heineken', slug='heineken', price=12.49, stock=50,
        description='uma boa cerveja!', category_slug=category_on_db.slug
    )

    service = ProductServices(db_session)

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
