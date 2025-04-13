from flowers_repository import FlowersRepository
class PurchasesRepository:
    purchases = []

    @classmethod
    def add_purchase(cls, user_id, flower_id):
        cls.purchases.append({"user_id": user_id, "flower_id": flower_id})

    @classmethod
    def get_purchases_by_user(cls, user_id):
        return [
            {"flower": flower, "price": flower.price}
            for purchase in cls.purchases if purchase["user_id"] == user_id
            for flower in FlowersRepository.flowers
            if flower.id == purchase["flower_id"]
        ]
