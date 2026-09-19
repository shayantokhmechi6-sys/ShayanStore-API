from sqlalchemy import Column, Integer , String,ForeignKey,Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id=Column(Integer , primary_key=True)
    username=Column(String(120), unique=True)
    password=Column(String(250))
    name=Column(String(15))
    mobile_phone=Column(String(11), unique=True)
    home_address=Column(String)
    is_admin=Column(Boolean,default=False)
    
class Product(Base):
    __tablename__ = "products"
    id=Column(Integer,primary_key=True)
    name=Column(String(20))
    price=Column(Integer)
    description=Column(String)
    stock=Column(Integer)
    
class Cart(Base):
    __tablename__ = "carts"
    id=Column(Integer , primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),unique=True)
    
class CartItem(Base):
    __tablename__ ="cart_items"
    id=Column(Integer,primary_key=True)
    product_id=Column(Integer,ForeignKey("products.id"))
    cart_id=Column(Integer,ForeignKey("carts.id"))
    quantity=Column(Integer)
    
class Order(Base):
    __tablename__ = "orders"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    status=Column(String)
    total_price=Column(Integer)
    
class OrderItem(Base):
    __tablename__ = "order_items"
    id=Column(Integer,primary_key=True)
    order_id=Column(Integer,ForeignKey("orders.id"))
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(Integer)
    
class Payment(Base):
    __tablename__ = "payments"
    id=Column(Integer,primary_key=True)
    order_id=Column(Integer , ForeignKey("orders.id"))
    amount=Column(Integer)
    gateway=Column(String)
    status=Column(String)