from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def update(self, item_id: int, data: dict):
        pass

    @abstractmethod
    async def delete(self, item_id: int):
        pass
    @abstractmethod
    async def retrieve(self, item_id: int):
        pass