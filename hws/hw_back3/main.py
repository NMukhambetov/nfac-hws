from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

cars = []

@app.get("/cars")
@app.get("/cars/search")
def search(request: Request, car_name: str = ""):
    result = [car for car in cars if car_name.lower() in car["name"].lower()]
    return templates.TemplateResponse("/search.html", {"request": request, "cars": result, "search_query": car_name})

@app.get("/cars/new")
def form(request: Request):
    return templates.TemplateResponse("/new.html", {"request": request})

@app.post("/cars/new")
def add(name: str = Form(...), year: int = Form(...)):
    cars.append({"name": name, "year": year})
    return RedirectResponse(url="/cars", status_code=303)

