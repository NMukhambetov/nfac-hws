from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, Session
from pydantic import BaseModel
from .database import Base

class Purchase(Base):
    __tablename__ = 'purchases'

    purchase_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    flower_id = Column(Integer, ForeignKey('flowers.flower_id'))

    user = relationship("User", back_populates="purchases")
    flower = relationship("Flower", back_populates="purchases")

# Pydantic модель для создания покупки
class PurchaseCreate(BaseModel):
    user_id: int
    flower_id: int

    model_config = {
        "from_attributes": True
    }

# Pydantic модель для ответа с покупкой
class PurchaseResponse(PurchaseCreate):
    purchase_id: int

    model_config = {
        "from_attributes": True
    }


class PurchaseRepository:
    def get_purchases_by_user(self, db: Session, user_id: int):
        return db.query(Purchase).filter(Purchase.user_id == user_id).all()

    def create_purchase(self, db: Session, purchase: PurchaseCreate):
        db_purchase = Purchase(
            user_id=purchase.user_id,
            flower_id=purchase.flower_id
        )
        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
