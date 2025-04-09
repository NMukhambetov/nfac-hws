from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

books = []

@app.get("/books", response_class=HTMLResponse)
def get_books(request: Request, page: int = 1):
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    page_books = books[start:end]

    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": page_books,
        "page": page,
        "has_prev": page > 1,
        "has_next": end < len(books)
    })

@app.get("/books/{book_id}", response_class=HTMLResponse)
def get_book(request: Request, book_id: int):
    for book in books:
        if book["id"] == book_id:
            return templates.TemplateResponse("book_detail.html", {"request": request, "book": book})
    return HTMLResponse(content="Not Found", status_code=404)

@app.get("/books/new", response_class=HTMLResponse)
def new_book_form(request: Request):
    return templates.TemplateResponse("new_book.html", {"request": request})


@app.post("/books", response_class=HTMLResponse)
def create_book(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    total_pages: int = Form(...),
    genre: str = Form(...)
):
    new_book = {
        "id": len(books) + 1,
        "title": title,
        "author": author,
        "year": year,
        "total_pages": total_pages,
        "genre": genre
    }
    books.append(new_book)
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": new_book})
