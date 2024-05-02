from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func


class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    slug = Column('slug', String(100), nullable=False)

    products = relationship(
        'Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    slug = Column('slug', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', Text, nullable=True)
    stock = Column('stock', Integer)
    category_id = Column('category_id', ForeignKey(
        Category.id, ondelete='SET NULL'), nullable=True)

    category = relationship(
        'Category', back_populates='products')
    orders = relationship('Order', secondary='order_items',
                          back_populates='products')


class Check(Base):
    __tablename__ = 'checks'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    in_use = Column('in_use', Boolean, nullable=False, default=False)

    orders = relationship(
        'Order', back_populates='check')


class Order(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    date_time = Column('date_time', DateTime, server_default=func.now())
    status = Column('status', Integer, nullable=False)
    check_id = Column('check_id', ForeignKey(Check.id, ondelete='SET NULL'), nullable=True)

    check = relationship('Check', back_populates='orders')
    products = relationship(
        'Product', secondary='order_items', back_populates='orders')


class Client(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    number = Column('number', String(20), nullable=True)
    cpf = Column('cpf', String(11), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    username = Column('username', String(40), nullable=False, unique=True)
    email = Column('email', String(100), nullable=False)
    password = Column('password', String(255), nullable=False)
    is_staff = Column('is_staff', Boolean, nullable=False, default=False)


class OrderItem(Base):
    __tablename__ = 'order_items'
    order_id = Column('order_id', ForeignKey(Order.id),
                      nullable=False, primary_key=True)
    product_id = Column('product_id', ForeignKey(
        Product.id), nullable=False, primary_key=True)
    quantity = Column('quantity', Integer, nullable=False)
