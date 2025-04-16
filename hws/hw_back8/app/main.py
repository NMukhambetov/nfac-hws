from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .users_repository import UserRepository, UserCreate, UserResponse
from .flowers_repository import FlowerRepository, FlowerCreate, FlowerResponse
from .purchase_repository import PurchaseRepository, PurchaseCreate, PurchaseResponse

app = FastAPI()
users_repo = UserRepository()
flowers_repo = FlowerRepository()
purchase_repo = PurchaseRepository()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Signup Route
@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_repo.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_repo.create_user(db, user)

# 2. Login Route
@app.post("/login", response_model=None)
def login(email: str, password: str, db: Session = Depends(get_db)):
    db_user = users_repo.get_user_by_email(db, email)
    if not db_user or db_user.password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

# 3. Profile Route
@app.get("/profile", response_model=UserResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    db_user = users_repo.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 4. Flowers Routes
@app.get("/flowers", response_model=List[FlowerResponse])
def get_flowers(db: Session = Depends(get_db)):
    return flowers_repo.get_all_flowers(db)

@app.post("/flowers", response_model=FlowerResponse)
def create_flower(flower: FlowerCreate, db: Session = Depends(get_db)):
    return flowers_repo.create_flower(db, flower)

@app.patch("/flowers/{flower_id}", response_model=FlowerResponse)
def update_flower(flower_id: int, updates: dict, db: Session = Depends(get_db)):
    updated_flower = flowers_repo.update_flower(db, flower_id, updates)
    if not updated_flower:
        raise HTTPException(status_code=404, detail="Flower not found")
    return updated_flower

@app.delete("/flowers/{flower_id}", response_model=None)
def delete_flower(flower_id: int, db: Session = Depends(get_db)):
    result = flowers_repo.delete_flower(db, flower_id)
    if not result:
        raise HTTPException(status_code=404, detail="Flower not found")
    return result

# 5. Purchased Routes
@app.post("/purchased", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    return purchase_repo.create_purchase(db, purchase)

@app.get("/purchased", response_model=List[PurchaseResponse])
def get_purchased_items(user_id: int, db: Session = Depends(get_db)):
    return purchase_repo.get_purchases_by_user(db, user_id)
