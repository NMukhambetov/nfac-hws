from ..models import User

class UserRepository:
    users = []
    _id_counter = 1

    @classmethod
    def add_user(cls, user: User):
        user.id = cls._id_counter
        cls.users.append(user)
        cls._id_counter += 1

    @classmethod
    def get_user_by_email(cls, email: str):
        for user in cls.users:
            if email == user.email:
                return user
        return None

    @classmethod
    def get_user_by_id(cls, user_id: int):
        for user in cls.users:
            if user.id == user_id:
                return user
        return None
