from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from database import engine,Base
from models import User,Product,Order,Cart,CartItem,Payment,OrderItem
from schemas import UserCreate,UserResponse,UserUpdate,ProductResponse,ProductCreate,ProductUpdate,OrderCreate,OrderResponse,CartResponse,CartItemCreate,CartItemResponse,CartItemUpdate,PaymentCreate,PaymentResponse,UserLogin,OrderItemResponse,AdminCreate
from security import password_hash,SECRET_KEY,ALGORITM,jwt,OAuth2PasswordBearer,oauth2_scheme
from datetime import datetime,timedelta
app=FastAPI()

Base.metadata.create_all(engine)

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITM])
    user_id=payload["user_id"]
    db_get_user=db.query(User).filter(User.id==user_id).first()
    if not db_get_user:
        raise HTTPException(status_code=404 , detail="User not found")
    return db_get_user

def get_current_admin(current_user:User=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403 , detail="User cannot access")
    return current_user
    

@app.get("/profile", response_model=UserResponse)
def get_profile(current_user:User=Depends(get_current_user)):
    return current_user

@app.post("/users" , response_model=UserResponse)
def create_user(user:UserCreate , db:Session=Depends(get_db)):
    hashed_password=password_hash.hash(user.password)
    existing_user=db.query(User).filter(User.username==user.username).first()
    if existing_user:
        raise HTTPException(status_code=400 , detail="User already exists")
    new_user=User(
        username=user.username,
        password=hashed_password,
        name=user.name,
        mobile_phone=user.mobile_phone,
        home_address=user.home_address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{
        "id":new_user.id,
        "username":new_user.username,
        "name":new_user.name,
        "mobile_phone":new_user.mobile_phone,
        "home_address":new_user.home_address
    }

@app.post("/login")
def login(user:UserLogin , db:Session=Depends(get_db)):
    db_login=db.query(User).filter(User.username==user.username).first()
    if not db_login:
        raise HTTPException(status_code=401 , detail="Invalid username or password")
    existing_password=password_hash.verify(user.password,db_login.password)
    if not existing_password:
        raise HTTPException(status_code=401 , detail="Invalid username or  password")
    expire_time=datetime.now()+timedelta(minutes=30)
    payload={
        "user_id":db_login.id,
        "exp":expire_time.timestamp()
    }
    token=jwt.encode(payload,SECRET_KEY,ALGORITM)
    return{
        "access_token":token
    }

@app.post("/admin", response_model=UserResponse)
def admin(admin:AdminCreate, db:Session=Depends(get_db)):
    db_admin=db.query(User).filter(User.is_admin==True).first()
    if db_admin:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    hashed_password=password_hash.hash(admin.password)
    new_user=User(
        username=admin.username,
        password=hashed_password,
        name=admin.name,
        mobile_phone=admin.mobile_phone,
        home_address=admin.home_address,
        is_admin=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@app.get("/users", response_model=list[UserResponse])
def get_user(current_user:User=Depends(get_current_admin),db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users

@app.get("/users/{user_id}" , response_model=UserResponse)
def users(user_id:int ,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404 , detail="User not found")
    if not user.id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    return user

@app.put("/users/{user_id}",response_model=UserResponse)
def update_user(user_id:int,user:UserUpdate,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404 , detail="User not found")
    if db_user.id!=current_user.id:
        raise HTTPException(status_code=403 , detail="User cannot access")
    db_user.username=user.username
    db_user.name=user.name
    db_user.mobile_phone=user.mobile_phone
    db_user.home_address=user.home_address
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id:int ,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404 , detail="Users not found")
    if not user.id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    db.delete(user)
    db.commit()
    return{
        "message":"User deleted successfully"
    }
    
@app.post("/products", response_model=ProductResponse)
def create_products(product:ProductCreate,current_user:User=Depends(get_current_admin) , db:Session=Depends(get_db)):
    new_product=Product(
        name=product.name,
        price=product.price,
        description=product.description,
        stock=product.stock
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products" , response_model=list[ProductResponse])
def get_product(db:Session=Depends(get_db)):
    product=db.query(Product).all()
    return product

@app.get("/product/{product_id}" , response_model=ProductResponse)
def products(product_id:int , db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404 , detail="Product not found")
    return product

@app.put("/products/{product_id}" , response_model=ProductResponse)
def update_product(product_id:int , product:ProductUpdate ,current_user:User=Depends(get_current_admin), db:Session=Depends(get_db)):
    db_product=db.query(Product).filter(Product.id==product_id).first()
    if not db_product:
        raise HTTPException(status_code=404 , detail="Product not found")
    db_product.name=product.name
    db_product.price=product.price
    db_product.description=product.description
    db_product.stock=product.stock
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id:int ,current_user:User=Depends(get_current_admin), db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=404 , detail="product not found")
    db.delete(product)
    db.commit()
    return{
        "message":"Product deleted successfully"
    },200  
    
@app.post("/order" , response_model=OrderResponse)
def create_order(current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not db_cart:
        raise HTTPException(status_code=404 , detail="Cart not found")
    cart_items=db.query(CartItem).filter(CartItem.cart_id==db_cart.id).all()
    if not cart_items:
        raise HTTPException(status_code=404 , detail="CartItem not found")
    for cart_item in cart_items:
        product=db.query(Product).filter(Product.id==cart_item.product_id).first()
        if not product:
            raise HTTPException(status_code=404 , detail="Product not found")
        if cart_item.quantity>product.stock:
            raise HTTPException(status_code=400 , detail="You request more than available stock")
        product.stock-=cart_item.quantity
            
    total_price=0
    for cart_item in cart_items:
        db_cart_items=db.query(Product).filter(Product.id==cart_item.product_id).first()
        total_price+=db_cart_items.price*cart_item.quantity
    new_order=Order(
        user_id=current_user.id,
        status="pending",
        total_price=total_price
    )
    db.add(new_order)
    db.flush()
    for cart_item in cart_items:
        new_order_item=OrderItem(
           order_id=new_order.id,
           product_id=cart_item.product_id,
           quantity=cart_item.quantity
        )
        db.add(new_order_item)
    for cart_item in cart_items:
        db.delete(cart_item)
    db.commit()
    db.refresh(new_order)
    return new_order
    
@app.get("/order", response_model=list[OrderResponse])
def get_order(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    order=db.query(Order).filter(Order.user_id==current_user.id).all()
    if not order:
        raise HTTPException(status_code=404 , detail="Order not found")
    return order

@app.get("/order/{order_id}" , response_model=OrderResponse)
def order(order_id:int,current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="Order not found")
    if not order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="User cannot access")
    return order

@app.post("/cart", response_model=CartResponse)
def create_cart(current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    db_cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not db_cart:
        db_cart=Cart(
            user_id=current_user.id
        )
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
        return db_cart
    raise HTTPException(status_code=400 , detail="Cart already exists")

@app.post("/cart-item" , response_model=CartItemResponse)
def create_cartitem(cartitem:CartItemCreate, current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==cartitem.product_id).first()
    if not product:
        raise HTTPException(status_code=404 , detail="Product not found")
    db_cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()
    if not db_cart:
        raise HTTPException(status_code=404 , detail="Cart not found")
    existing_item=db.query(CartItem).filter(CartItem.product_id==cartitem.product_id, CartItem.cart_id==db_cart.id).first()
    if existing_item:
        raise HTTPException(status_code=400 , detail="Product already exists in cart ")
         
    new_CartItem=CartItem(
        product_id=cartitem.product_id,
        cart_id=db_cart.id,
        quantity=cartitem.quantity
    )
    db.add(new_CartItem)
    db.commit()
    db.refresh(new_CartItem)
    return new_CartItem

@app.get("/cart", response_model=list[CartResponse])
def get_carts(current_user:User=Depends(get_current_user),db: Session = Depends(get_db)):
    carts = db.query(Cart).filter(Cart.user_id==current_user.id).all()
    if not carts:
        raise HTTPException(status_code=404 , detail="Carts not found")
    return carts

@app.get("/cart_items" , response_model=list[CartItemResponse])
def get_cart_items(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    cart_items=db.query(CartItem).join(Cart).filter(Cart.user_id==current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=404 , detail="Cart items not found")
    return cart_items

@app.get("/cart_items/{cart_item_id}" , response_model=CartItemResponse)
def cart_items(cart_item_id:int ,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    cart_item=db.query(CartItem).filter(CartItem.id==cart_item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404 , detail="CartItem not found")
    db_cart=db.query(Cart).filter(Cart.id==cart_item.cart_id).first()
    if not db_cart.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    return{
        "id":cart_item.id,
        "product_id":cart_item.product_id,
        "cart_id":cart_item.cart_id,
        "quantity":cart_item.quantity
    }

@app.put("/cart_items/{cart_item_id}" , response_model=CartItemResponse)
def update_cart_items(cart_item_id:int ,cart_item:CartItemUpdate,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_cart_item=db.query(CartItem).filter(CartItem.id==cart_item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404 , detail="cart_item not found")
    db_cart=db.query(Cart).filter(Cart.id==db_cart_item.cart_id).first()
    if not db_cart.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="users cannot access")
    db_cart_item.quantity=cart_item.quantity
    
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@app.delete("/cart_items/{cart_item_id}")
def delete_cart_item(cart_item_id:int ,current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_cart_item=db.query(CartItem).filter(CartItem.id==cart_item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404 , detail="CartItem not found")
    db_cart=db.query(Cart).filter(Cart.id==db_cart_item.cart_id).first()
    if not db_cart.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    db.delete(db_cart_item)
    db.commit()
    return{
        "message":"CartItem deleted successfully"
    }

@app.get("/order/{order_id}/items", response_model=list[OrderItemResponse])
def get_order_items(order_id:int , current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_order=db.query(Order).filter(Order.id==order_id).first()
    if not db_order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    db_order_item=db.query(OrderItem).filter(OrderItem.order_id==order_id).all()
    if not db_order_item:
        raise HTTPException(status_code=404 , detail="OrderItem not found")
    return db_order_item
    
    
@app.put("/order/{order_id}/cancel" , response_model=OrderResponse)
def cancel_order(order_id:int , current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_order=db.query(Order).filter(Order.id==order_id).first()
    if not db_order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    if not db_order.status=="pending":
        raise HTTPException(status_code=400 , detail="Only pending orders can be cancelled")
    db_order_items=db.query(OrderItem).filter(OrderItem.order_id==order_id).all()
    for item in db_order_items:
        product_id=item.product_id
        quantity=item.quantity
        product=db.query(Product).filter(Product.id==product_id).first()
        product.stock+=quantity
    db_order.status="cancelled"
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/order/{order_id}")
def delete_order(order_id:int,current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if not order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="User cannot access")
    if order.status=="paid":
        raise HTTPException(status_code=400 , detail="Paid orders cannot be deleted")
    if order.status=="pending":
        db_order_items=db.query(OrderItem).filter(OrderItem.order_id==order_id).all()
        for item in db_order_items:
            product=db.query(Product).filter(Product.id==item.product_id).first()
            product.stock+=item.quantity
    db.delete(order)
    db.commit()
    return {
        "message":"Order deleted successfully"
    }
    
@app.post("/payment", response_model=PaymentResponse)
def create_payment(payment:PaymentCreate,current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    db_order=db.query(Order).filter(Order.id==payment.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="User cannot access")
    db_payment=db.query(Payment).filter(Payment.order_id==payment.order_id).first()
    if db_payment:
        raise HTTPException(status_code=400 , detail="Payment already exists")
    
    new_payment=Payment(
        order_id=payment.order_id,
        amount=db_order.total_price,
        gateway=payment.gateway,
        status="pending"
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@app.get("/payments", response_model=list[PaymentResponse])
def get_payment(current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_payment=db.query(Payment).join(Order).filter(Order.user_id==current_user.id).all()
    if not db_payment:
        raise HTTPException(status_code=404 , detail="Payment not found")
    return db_payment

@app.get("/payment/{payment_id}", response_model=PaymentResponse)
def payment(payment_id:int, current_user:User=Depends(get_current_user) ,  db:Session=Depends(get_db)):
    payment=db.query(Payment).join(Order).filter(Payment.id==payment_id).first()
    if not payment:
        raise HTTPException(status_code=404 , detail="Payment not found")
    db_order=db.query(Order).filter(Order.id==payment.order_id).first()
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    return{
        "id":payment.id,
        "order_id":payment.order_id,
        "amount":payment.amount,
        "gateway":payment.gateway,
        "status":payment.status
    }
    

@app.delete("/payment/{payment_id}")
def delete_payment(payment_id:int,current_user:User=Depends(get_current_user) , db:Session=Depends(get_db)):
    db_payment=db.query(Payment).filter(Payment.id==payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404 , detail="Payment not found")
    db_order=db.query(Order).filter(Order.id==db_payment.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users Cannot access")
    db.delete(db_payment)
    db.commit()
    return{
        "message":"Payment deleted successfully"
    }
    
@app.put("/payment/{payment_id}/verify")
def verify_payment(payment_id:int , current_user:User=Depends(get_current_user), db:Session=Depends(get_db)):
    db_payment=db.query(Payment).filter(Payment.id==payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404 , detail="Payment not found")
    if not db_payment.status=="pending":
        raise HTTPException(status_code=400 , detail="Only pending payments can be verified")
    db_order=db.query(Order).filter(Order.id==db_payment.order_id).first()
    if not db_order:
        raise HTTPException(status_code=404 , detail="Order not found")
    if db_order.status=="cancelled":
        raise HTTPException(status_code=400 , detail="Cancelled orders cannot be paid")
    if not db_order.user_id==current_user.id:
        raise HTTPException(status_code=403 , detail="Users cannot access")
    db_payment.status="paid"
    db_order.status="paid"
    db.commit()
    db.refresh(db_payment)
    db.refresh(db_order)
    return db_payment
        
    
    