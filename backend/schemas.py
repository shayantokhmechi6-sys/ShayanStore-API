from pydantic import BaseModel,ConfigDict,Field

class UserCreate(BaseModel):
    username:str
    password:str
    name:str
    mobile_phone:str
    home_address:str

class AdminCreate(BaseModel):
    username:str
    password:str
    name:str
    mobile_phone:str
    home_address:str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    username:str
    name:str
    mobile_phone:str
    home_address:str

class UserUpdate(BaseModel):
    username:str
    name:str
    mobile_phone:str
    home_address:str

    
class ProductCreate(BaseModel):
    name:str
    price:int=Field(ge=0)
    description:str
    stock:int=Field(ge=0)
    
class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    name:str
    price:int
    description:str
    stock:int
class ProductUpdate(BaseModel):
    name:str
    price:int=Field(ge=0)
    description:str
    stock:int=Field(ge=0)

    
class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    
class CartItemCreate(BaseModel):
    product_id:int
    quantity:int=Field(ge=1)
    
class CartItemUpdate(BaseModel):
    quantity:int=Field(ge=1)
    
class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    product_id:int
    cart_id:int
    quantity:int

class OrderCreate(BaseModel):
    pass
   

class OrderUpdate(BaseModel):
    status:str
    
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    status:str
    total_price:int
    
class OrderItemCreate(BaseModel):
    order_id:int
    product_id:int
    quantity:int

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    order_id:int
    product_id:int
    quantity:int
    
class PaymentCreate(BaseModel):
    order_id:int
    gateway:str

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    order_id:int
    amount:int
    gateway:str
    status:str
    
class UserLogin(BaseModel):
    username:str
    password:str
    
    
    