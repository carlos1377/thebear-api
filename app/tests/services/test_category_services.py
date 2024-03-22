from app.services.category_services import CategoryServices
from app.schemas.category import Category
from app.db.models import Category as CategoryModel


def test_category_add_service(db_session):
    service = CategoryServices(db_session)

    category = Category(
        name='Destilado',
        slug='destilado'
    )

    service.add_category(category=category)

    category_on_db = db_session.query(CategoryModel).all()

    assert len(category_on_db) == 1
    assert category_on_db[0].name == 'Destilado'
    assert category_on_db[0].slug == 'destilado'

    db_session.delete(category_on_db[0])
    db_session.commit()


def test_category_list_service(db_session, categories_on_db):
    service = CategoryServices(db_session)

    categories = service.list_categories()

    assert len(categories) == 4
    assert categories[0].name == 'Bebida'
    assert categories[3].slug == 'bebida-sem-alcool'
