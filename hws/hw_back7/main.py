from fastapi import FastAPI, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, List
import jwt
from datetime import datetime, timedelta
app = FastAPI()

users_db = {
    "test@example.com": {"first_name": "Test", "email": "test@example.com", "password": "password123"}
}
flowers_db = []
purchased_db = {}
cart_db = {}

SECRET_KEY = "MNM"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

class User(BaseModel):
    first_name: str
    email: str
    password: str

class Flower(BaseModel):
    id: int
    name: str
    quantity: int
    price: int

class FlowerIn(BaseModel):
    name: str
    quantity: int
    price: int

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid user")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/signup")
def signup(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = user.dict()
    return {"message": "User created successfully"}

@app.post("/api/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/profile")
def get_profile(email: str = Depends(get_user_from_token)):
    return users_db[email]

@app.get("/api/flowers", response_model=List[Flower])
def list_flowers():
    return flowers_db

@app.post("/api/flowers", response_model=Flower)
def add_flower(flower: FlowerIn):
    new_id = len(flowers_db) + 1
    new_flower = Flower(id=new_id, **flower.dict())
    flowers_db.append(new_flower)
    return new_flower

@app.post("/api/cart/items")
def add_to_cart(flower_id: int, cart: Optional[str] = Cookie(default="")):
    updated_cart = cart + f"{flower_id},"
    return {"message": "Added to cart", "cart_cookie": updated_cart}

@app.get("/api/cart/items")
def view_cart(cart: Optional[str] = Cookie(default="")):
    if not cart:
        return {"flowers": [], "total": 0}
    ids = list(map(int, cart.strip(",").split(",")))
    selected = [flower for flower in flowers_db if flower.id in ids]
    total = sum(f.price for f in selected)
    return {"flowers": selected, "total": total}

@app.post("/api/purchase")
def purchase(email: str = Depends(get_user_from_token), cart: Optional[str] = Cookie(default="")):
    if not cart:
        return {"message": "Cart is empty"}
    ids = list(map(int, cart.strip(",").split(",")))
    selected = [flower for flower in flowers_db if flower.id in ids]
    purchased_db.setdefault(email, []).extend(selected)
    return {"message": "Purchase successful"}

@app.get("/api/purchased")
def get_purchased(email: str = Depends(get_user_from_token)):
    return purchased_db.get(email, [])
