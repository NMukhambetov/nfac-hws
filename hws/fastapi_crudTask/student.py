from fastapi import FastAPI, HTTPException
import asyncpg

app = FastAPI()

DATABASE_URL = "postgresql://postgres:nurtas05@localhost:5432/postgres"

async def get_db():
    return await asyncpg.connect(DATABASE_URL)

@app.post("/student")
async def create_student(name: str, gpa: float, study_year: int, department: str):
    db = await get_db()
    try:
        query = """
            INSERT INTO students (name, gpa, study_year, department) 
            VALUES ($1, $2, $3, $4) RETURNING id, name, gpa, study_year, department
        """
        return await db.fetchrow(query, name, gpa, study_year, department)
    finally:
        await db.close()


@app.get("/students")
async def get_students():
    db = await get_db()
    try:
        return await db.fetch("SELECT * FROM students")
    finally:
        await db.close()


@app.get("/student/{student_id}")
async def get_student(student_id: int):
    db = await get_db()
    try:
        student = await db.fetchrow("SELECT * FROM students WHERE id = $1", student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    finally:
        await db.close()


# @app.patch("/student/{student_id}")
# async def update_student(student_id: int, name: str = None, gpa: float = None, study_year: int = None, department: str = None):
#     db = await get_db()
#     try:
#        updates = []
#        values = []
#        for i , (key,value) in enumerate(data_items):
#            updates.append((f"{key} = ${i+1}"))
#            values.append(value)
#
#        values.append(student_id)
#         query = f"UPDATE students SET {', '.join(update_fields)} WHERE id = ${len(values)} RETURNING *"
# return await db.fetchrow(query, *values)
# finally:
# await db.close()


@app.delete("/student/{student_id}")
async def delete_student(student_id: int):
    db = await get_db()
    try:
        result = await db.execute("DELETE FROM students WHERE id = $1", student_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted"}
    finally:
        await db.close()
