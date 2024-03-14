from app.db.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    slug = Column('slug', String(100), nullable=False)

    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    slug = Column('slug', String(100), nullable=False)
    price = Column('price', Float)
    description = Column('description', Text, nullable=True)
    category_id: Column = Column(
        'category_id', ForeignKey(Category.id), nullable=False)

    category = relationship('Category', back_populates='products')
    order = relationship('Order', back_populates='products')
    order_item = relationship('OrderItem', back_populates='product')


class Order(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    date_time = Column('date_time', DateTime, server_default=func.now())
    order_items: Column = Column(
        'order_items', ForeignKey(Product.id), nullable=False)
    status = Column('status', String(40), nullable=False)
    total = Column('total', Float)

    products = relationship('Product', back_populates='order')
    order_item = relationship('OrderItem', back_populates='order')


class Client(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    name = Column('name', String(60), nullable=False)
    email = Column('email', String(100), nullable=False)
    number = Column('number', String(20), nullable=True)


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    id_order: Column = Column('id_order', ForeignKey(Order.id), nullable=False)
    id_product: Column = Column(
        'id_product', ForeignKey(Product.id), nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    unittprice = Column('unittprice', Float)
    total = Column('total', Float)

    order = relationship('Order', back_populates='order_item')
    product = relationship('Product', back_populates='order_item')
