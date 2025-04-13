from ..models import Flower
class FlowersRepository:
    flowers = []
    _id_counter = 1
    @classmethod
    def add_flower(cls, flower: Flower):
        flower.id = cls._id_counter
        cls.flowers.append(flower)
        cls._id_counter += 1
    @classmethod
    def get_all_flowers(cls):
        return cls.flowers

    @classmethod
    def get_flower_by_id(cls, flower_id:int):
        for flower in cls.flowers:
            if flower.id == flower_id:
                return flower
        return "Flower not found or does not exist"
