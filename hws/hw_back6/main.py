from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from hw_back6.models import User
from hw_back6.models import Flower
from hw_back6.models import Purchase
from hw_back6.repositories.users_repository import UserRepository
from hw_back6.repositories.flowers_repository import FlowersRepository
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="hw_back6/templates")
app.mount("/hws/hw_back6/static", StaticFiles(directory="/home/nfac-hws/hws/hw_back6/static"), name="static")
SECRET_KEY = "MNM"

def create_jwt_token(user_id):
    body={"user_id":user_id}
    token = jwt.encode(body,SECRET_KEY,algorithm="HS256")
    return token

def decode_jwt_token(token):
    try:
        body = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return body
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")

def get_flowers_from_cart(request: Request):
    cart = request.cookies.get("cart")
    if not cart:
        return []
    flower_ids = cart.split(",")
    flowers = []
    for flower_id in flower_ids:
        flower = FlowersRepository.get_flower_by_id(int(flower_id))
        if flower:
            flowers.append(flower)
    return flowers
@app.get("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_post(
    request: Request,
    name : str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):

    user = User(first_name=name, email=email,password=password)
    UserRepository.add_user(user)

    return RedirectResponse("/login",status_code = 303)

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(
    request: Request,
    email:str = Form(...),
    password:str = Form(...),
):
   user = UserRepository.get_user_by_email(email)
   if user.password == password:
       token = create_jwt_token(user.user_id)
       response = RedirectResponse("/profile",status_code = 303)
       response.set_cookie("token",token)
       return response
   return templates.TemplateResponse("login.html",
    {"request": request,
     "error" :"Invalid email or password"
    })

@app.get("/profile")
def profile(request: Request):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=401,detail="Authentication required")
    body = decode_jwt_token(token)
    user_id = body.get("id")

    user = UserRepository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401,detail="User not found")

    return templates.TemplateResponse("profile.html", {"request": request,})

@app.get("/flowers" , response_class=HTMLResponse)
def get_flowers(request: Request):
    flowers = FlowersRepository.get_all_flowers()
    return templates.TemplateResponse("flowers.html", {"request": request , "flowers":flowers})

@app.post("/flowers")
def create_flower(
    request: Request,
    flower_name : str = Form(...),
    quantity:int = Form(...),
    price:int = Form(...),
):
    flowers = Flower(flower_name,quantity,price)
    FlowersRepository.add_flower(flowers)
    return RedirectResponse("/flowers",status_code = 303)

@app.post("/cart/items")
async def add_cart_items(
    request: Request,
    flower_id:int = Form(...),
):
    cart_cookie = request.cookies.get("cart","")

    new_cart = f"{cart_cookie},{flower_id}" if cart_cookie else str(flower_id)

    response = RedirectResponse("/flowers",status_code = 303)
    response.set_cookie("cart",new_cart)

    return response

@app.get("/cart/items")
def view_carts(request: Request):
    cart_cookie = request.cookies.get("cart","")

    if not cart_cookie:
        return templates.TemplateResponse("cart.html", {"request": request, "flowers": [], "total": 0})

    flower_ids = []

    flower_id_strings = cart_cookie.split(",")

    for flower_id_str in flower_id_strings:
        flower_ids.append(int(flower_id_str))

    flowers_in_cart = []
    total_price  = 0
    for flower_id in flower_ids:
        flower = FlowersRepository.get_flower_by_id(flower_id)
        if flower:
            flowers_in_cart.append(flower)
            total_price += flower.price * flower.quantity

    return templates.TemplateResponse("cart.html", {
    "request": request,
    "flowers": flowers_in_cart,
    "total": total_price
    })

@app.post("/purchased")
def purchase_post(request:Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        decoded_token = decode_jwt_token(token)
        user_id = decoded_token.get("user_id")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    flowers_in_cart = get_flowers_from_cart(request)
    if not flowers_in_cart:
        raise HTTPException(status_code=401, detail="No flowers in cart")

    for flower in flowers_in_cart:
        PurchasesRepository.add_purchase(user_id,flower.id)

    response = RedirectResponse("/purchased",status_code = 303)
    response.delete_cookie("cart")

    return response

@app.get("/purchased")
async def get_purchased(request:Request):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        decoded_token = decode_jwt_token(token)
        user_id = decoded_token.get("user_id")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    purchased_flowers = PurchasesRepository.get_purchases_by_user(user_id)
    if not purchased_flowers:
        raise HTTPException(status_code=401, detail="No purchases found")

    return templates.TemplateResponse("purchased.html", {"request": request, "purchased_flowers": purchased_flowers})
