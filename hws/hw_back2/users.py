from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

users = [
    {"id": 1, "email": "test@test.com", "first_name": "Aibek", "last_name": "Bekturov", "username": "deadly_knight95"},
    {"id": 2, "email": "example@example.com", "first_name": "John", "last_name": "Doe", "username": "johnny_d"},
]

@app.get("/users", response_class=HTMLResponse)
def get_users():
    html_content = "<table border='1'>"
    for user in users:
        html_content += f"<tr><td>{user['username']}</td><td><a href='/users/{user['id']}'>{user['first_name']} {user['last_name']}</a></td></tr>"
    html_content += "</table>"
    return html_content
@app.get("/users/{id}", response_class=HTMLResponse)
def get_user_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return f"""
            <h1>{user['first_name']} {user['last_name']}</h1>
            <p><b>Username:</b> {user['username']}</p>
            <p><b>Email:</b> {user['email']}</p>
            """
    raise HTTPException(status_code=404, detail="Not found")