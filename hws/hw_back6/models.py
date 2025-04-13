class User:
    def __init__(self, first_name,email, password):
        self.id = None
        self.first_name = first_name
        self.email = email
        self.password = password

class Flower:
    def __init__(self,flower_name:str,quantity:int,price:float):
        self.flower_name = flower_name
        self.quantity = quantity
        self.price = price

class Purchase:
    def __init__(self,user_id:int,flower_id:int):
        self.user_id = user_id
        self.flower_id = flower_id
