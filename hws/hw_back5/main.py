from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

books = [
    {"id": 1, "title": "Book One", "author": "Author A"},
    {"id": 2, "title": "Book Two", "author": "Author B"},
]


@app.get("/books/{id}/edit")
def update_books(request: Request, id: int):
    for book in books:
        if book["id"] == id:
            return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books/{id}/edit")
def update_books_post(id: int, title: str = Form(...), author: str = Form(...)):
    for book in books:
        if book["id"] == id:
            book["title"] = title
            book["author"] = author
            return RedirectResponse(url=f"/books/{id}", status_code=302)
        raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/{id}/delete")
def delete_book(id:int):
    for index,book in enumerate(books):
        if book["id"] == id:
            books.pop(index)
            return RedirectResponse(url=f"/books", status_code=302)
        raise HTTPException(status_code=404, detail="Book not found")