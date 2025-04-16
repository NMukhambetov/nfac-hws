from sqlalchemy import Integer, Column, String, Float
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from .database import Base

class Flower(Base):
    __tablename__ = 'flowers'

    flower_id = Column(Integer, primary_key=True)
    flower_name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

    purchases = relationship("Purchase", back_populates="flower")

# Pydantic модель для создания цветка
class FlowerCreate(BaseModel):
    flower_name: str
    quantity: int
    price: float

    model_config = {
        "from_attributes": True
    }

# Pydantic модель для ответа с цветком
class FlowerResponse(FlowerCreate):
    flower_id: int

    model_config = {
        "from_attributes": True
    }

class FlowerRepository:
        def get_flower(self, db: Session, flower_id: int):
            return db.query(Flower).filter(Flower.flower_id == flower_id).first()

        def get_all_flowers(self, db: Session, skip: int = 0, limit: int = 100):
            return db.query(Flower).offset(skip).limit(limit).all()

        def create_flower(self, db: Session, flower: FlowerCreate):
            db_flower = Flower(
                flower_name=flower.flower_name,
                quantity=flower.quantity,
                price=flower.price
            )
            db.add(db_flower)
            db.commit()
            db.refresh(db_flower)
            return db_flower

        def update_flower(self, db: Session, flower_id: int, updates: dict):
            flower = db.query(Flower).filter(Flower.flower_id == flower_id).first()
            if not flower:
                return None
            for key, value in updates.items():
                setattr(flower, key, value)
            db.commit()
            db.refresh(flower)
            return flower

        def delete_flower(self, db: Session, flower_id: int):
            flower = db.query(Flower).filter(Flower.flower_id == flower_id).first()
            if not flower:
                return None
            db.delete(flower)
            db.commit()
            return {"message": "Flower deleted successfully"}
