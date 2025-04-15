import asyncio
import asyncpg
from hws.db_repository.asyncpg_repository import AsyncpgRepository

async def create_tables():
    conn = await asyncpg.connect(user='postgres', password='nurtas05', host='localhost', port='5432', database='postgres')
    await conn.execute('DROP TABLE IF EXISTS users;')
    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name VARCHAR(255),
            role VARCHAR(255),
            gpa NUMERIC(3,2),
            study_year INTEGER,
            department VARCHAR(255)
        )
    ''')
    await conn.close()

async def main():
    await create_tables()

    conn = await asyncpg.connect(user='postgres', password='nurtas05', host='localhost', port='5432', database='postgres')
    repo = AsyncpgRepository(conn)

    await repo.create({"name": "Nurtas", "role": "student", "gpa": 3.5, "study_year": 2, "department": "Computer Science"})
    await repo.create({"name": "Erasyl", "role": "teacher", "gpa": 3.7, "study_year": 4, "department": "Pedagogy"})

    print("\n--- Users after creation ---")
    users = await repo.get_all()
    for user in users:
        print(dict(user))

    user = await repo.retrieve(1)
    print("\n--- Retrieved User (ID=1) ---")
    print(dict(user))

    await repo.update(1, {"gpa": 3.9, "study_year": 3})

    print("\n--- Users after update ---")
    users = await repo.get_all()
    for user in users:
        print(dict(user))

    await repo.delete(2)

    print("\n--- Users after deletion ---")
    users = await repo.get_all()
    for user in users:
        print(dict(user))

    await repo.create({"name": "Bektas", "role": "student", "gpa": 4.0, "study_year": 1, "department": "Finance"})
    print("\n ---User after add new user ---")
    users = await repo.get_all()
    for user in users:
        print(dict(user))
    await conn.close()


if __name__ == '__main__':
    asyncio.run(main())