from app.repositories.sqlalchemy.category_repository import DBCategoryRepository  # noqa
from app.services.category_services import CategoryServices
from app.db.models import Category as CategoryModel
from app.schemas.category import Category


def test_category_add_service(db_session):
    repository = DBCategoryRepository(db_session)

    service = CategoryServices(repository)

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


def test_list_category_service(db_session, categories_on_db):
    repository = DBCategoryRepository(db_session)

    service = CategoryServices(repository)

    categories = service.list_categories()

    assert len(categories) == 4
    assert categories[0].name == 'Bebida'
    assert categories[3].slug == 'bebida-sem-alcool'


def test_list_category_by_id_service(db_session, categories_on_db):
    category_id = categories_on_db[0].id

    repository = DBCategoryRepository(db_session)

    service = CategoryServices(repository)

    category = service.list_categories(id=category_id)

    assert category.id == category_id
    assert category.name == 'Bebida'
    assert category.slug == 'bebida'


def test_delete_category_service(db_session):
    category_model = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category_model)
    db_session.commit()

    repository = DBCategoryRepository(db_session)

    service = CategoryServices(repository)

    service.delete_category(id=category_model.id)

    categories_on_db = db_session.query(CategoryModel).all()

    assert len(categories_on_db) == 0


def test_update_category_service(db_session):
    category_model = CategoryModel(name='Roupa', slug='roupa')
    db_session.add(category_model)
    db_session.commit()

    category_id = db_session.query(CategoryModel).first().id

    repository = DBCategoryRepository(db_session)

    service = CategoryServices(repository)

    new_category = Category(name='Bebida', slug='bebida')

    service.update_category(id=category_id, category=new_category)

    category_updated_on_db = db_session.query(
        CategoryModel).filter_by(id=category_model.id).first()

    assert category_updated_on_db is not None
    assert category_updated_on_db.name == new_category.name
    assert category_updated_on_db.slug == new_category.slug

    db_session.delete(category_updated_on_db)
    db_session.commit()
