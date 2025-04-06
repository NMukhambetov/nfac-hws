from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

books = []
counter = 1

@app.get("/books")
def books_list(request: Request, page: int = 1):
    start = (page - 1) * 10
    end = start + 10
    return templates.TemplateResponse("books/index.html", {
        "request": request,
        "books": books[start:end],
        "page": page,
        "has_next": end < len(books),
        "has_prev": page > 1
    })

@app.get("/books/{id}")
def books_detail(request: Request, id: int):
    for book in books:
        if book["id"] == id:
            return templates.TemplateResponse("books/detail.html", {
                "request": request,
                "book": book
            })
    return templates.TemplateResponse("books/detail.html", {
        "request": request,
        "book": None
    }, status_code=404)

@app.get("/books/new")
def new_book_form(request: Request):
    return templates.TemplateResponse("books/new.html", {"request": request})

@app.post("/books")
def create_book(
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    total_pages: int = Form(...),
    genre: str = Form(...)
):
    global counter
    books.append({
        "id": counter,
        "title": title,
        "author": author,
        "year": year,
        "pages": total_pages,
        "genre": genre
    })
    counter += 1
    return RedirectResponse("/books", status_code=303)
