from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
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


class Order(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    date_time = Column('date_time', DateTime, server_default=func.now())
    status = Column('status', String(40), nullable=False)
    mesa = Column('mesa', Integer)

    products = relationship(
        'Product', secondary='order_items', back_populates='orders')


class Client(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    email = Column('email', String(100), nullable=False)
    number = Column('number', String(20), nullable=True)


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    id_order = Column('id_order', ForeignKey(Order.id), nullable=False)
    id_product = Column('id_product', ForeignKey(Product.id), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
