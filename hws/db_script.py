import asyncio
import asyncpg

async def get_connection():
    return await asyncpg.connect(user='postgres', password='nurtas05',host='localhost',port='5432',database='postgres')

async def create_tables():
    connect = await get_connection()
    await connect.execute('DROP TABLE IF EXISTS users;')
    await connect.execute('CREATE TABLE users(id serial PRIMARY KEY, name VARCHAR(255),role VARCHAR(255),gpa NUMERIC(3,2),study_year INTEGER,department VARCHAR(255))')
    await connect.close()
async def create_users(name,role,gpa,study_year,department):
    connect = await get_connection()
    await connect.execute('INSERT INTO users(name,role,gpa,study_year,department) VALUES($1,$2,$3,$4,$5)' , name,role,gpa,study_year,department)
    await connect.close()

async def delete_user(user_id=None):
    connect = await get_connection()
    await connect.execute("Delete from users where id=$1",user_id)
    await connect.close()
async def get_users():
    connect = await get_connection()
    await connect.execute('SELECT * from users')
    await connect.close()
async def retrieve(user_id):
    connect = await get_connection()
    await connect.fetch('SELECT * FROM users WHERE id = $1', user_id)
    await connect.close()
async def update_user(user_id, data: dict):
    connect = await get_connection()

    updates = []
    values = []

    for i, (key, value) in enumerate(data.items()):
        updates.append(f"{key} = ${i + 1}")
        values.append(value)

    values.append(user_id)
    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ${len(values)}"

    await connect.execute(query, *values)
    await connect.close()

async def main():
    await create_tables()

    await create_users("Nurtas","student",3.5,2,"Computer Science")
    await create_users("Erasyl", "teacher", 3.7, 4, "Pedogog")

if __name__ == '__main__':
    asyncio.run(main())



