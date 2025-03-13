from fastapi import FastAPI, Request , HTTPException

app = FastAPI()

cars = [
    {"id": 1, "name": "Toyota Camry", "year": "2020"},
    {"id": 2, "name": "Honda Civic", "year": "2018"},
    {"id": 3, "name": "Ford Focus", "year": "2019"},
    {"id": 4, "name": "Chevrolet Malibu", "year": "2021"},
]

@app.get("/cars")
def get_cars(request: Request):
    page = int(request.query_params.get("page", 1))
    limit = int(request.query_params.get("limit", 10))
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]

@app.get("/cars/{id}")
def get_car_by_id(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    raise HTTPException(status_code=404, detail="Not found")