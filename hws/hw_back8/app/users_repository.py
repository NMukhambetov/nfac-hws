from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from .database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String, unique=True, index=True)
    password = Column(String())

    purchases = relationship("Purchase", back_populates="user")

# Pydantic модель для создания пользователя
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    model_config = {
        "from_attributes": True
    }

# Pydantic модель для ответа с пользователем
class UserResponse(UserCreate):
    user_id: int

    model_config = {
        "from_attributes": True
    }

class UserRepository:
    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_all_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate):
        db_user = User(name=user.name, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


