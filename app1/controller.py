from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

# Prefix "/users" is added when registered in main.py
router = APIRouter(tags=["Users"])

# Request/Response Schemas (DTOs)
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

# Mock database for demonstration
fake_users_db = {
    1: {"id": 1, "username": "jdoe", "email": "jdoe@example.com"}
}

@router.get("/", response_model=list[UserResponse])
def get_all_users():
    return list(fake_users_db.values())

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    new_id = len(fake_users_db) + 1
    new_user = {"id": new_id, **payload.model_dump()}
    fake_users_db[new_id] = new_user
    return new_user
  
# Prefix "/orders" is added when registered in main.py
router = APIRouter(tags=["Orders"])

class OrderCreate(BaseModel):
    user_id: int
    item: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    item: str
    quantity: int
    status: str

fake_orders_db = {
    101: {"id": 101, "user_id": 1, "item": "Laptop", "quantity": 1, "status": "shipped"}
}

@router.get("/", response_model=list[OrderResponse])
def get_all_orders(user_id: int | None = None):
    orders = list(fake_orders_db.values())
    if user_id is not None:
        return [o for o in orders if o["user_id"] == user_id]
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    order = fake_orders_db.get(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order not found"
        )
    return order

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    new_id = max(fake_orders_db.keys(), default=100) + 1
    new_order = {
        "id": new_id,
        "status": "pending",
        **payload.model_dump()
    }
    fake_orders_db[new_id] = new_order
    return new_order