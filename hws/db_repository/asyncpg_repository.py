from base_repository import BaseRepository

class AsyncpgRepository(BaseRepository):
    def __init__(self, connection):
        self.connection = connection

    async def create(self, data: dict):
        await self.connection.execute('''
               INSERT INTO users(name, role, gpa, study_year, department)
               VALUES ($1, $2, $3, $4, $5)
           ''', data['name'], data['role'], data['gpa'], data['study_year'], data['department'])

    async def get_all(self):
        return await self.connection.fetch('SELECT * FROM users')

    async def retrieve(self, item_id: int):
        return await self.connection.fetchrow('SELECT * FROM users WHERE id = $1', item_id)

    async def update(self, item_id: int, data: dict):
        updates = []
        values = []

        for i, (key, value) in enumerate(data.items()):
            updates.append(f"{key} = ${i + 1}")
            values.append(value)

        values.append(item_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ${len(values)}"
        await self.connection.execute(query, *values)

    async def delete(self, item_id: int):
        await self.connection.execute('DELETE FROM users WHERE id = $1', item_id)