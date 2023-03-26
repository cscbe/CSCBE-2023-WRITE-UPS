from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError
from starlette.requests import Request
from fastapi.responses import RedirectResponse
import random
import time, threading
from threading import Lock
import uvicorn
import copy
import logging
import sys
import os

logger = logging.getLogger("Foodtruck")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.handlers.clear()
logger.addHandler(sh)

refresh_time = int(os.getenv("FRESH_TIME", "3"))
flag = os.getenv("FLAG", "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")

genLock = Lock()

recipes = {
    "Tomato Soup": ["Tomatoes", "Onion", "Garlic", "Chicken Broth"],
    "Mac and Cheese": ["Macaroni", "Cheese", "Milk", "Butter"],
    "Fried Rice": ["Rice", "Eggs", "Soy Sauce", "Vegetables"],
    "Scrambled Eggs": ["Eggs", "Milk", "Salt", "Pepper"],
    "BLT Sandwich": ["Bread", "Bacon", "Lettuce", "Tomato"],
    "Caesar Salad": [
        "Romaine Lettuce",
        "Croutons",
        "Parmesan Cheese",
        "Caesar Dressing",
    ],
    "Baked Potatoes": ["Potatoes", "Butter", "Salt", "Pepper"],
    "Spaghetti Carbonara": ["Spaghetti", "Pancetta", "Eggs", "Parmesan Cheese"],
    "Grilled Chicken": ["Chicken Breasts", "Olive Oil", "Salt", "Pepper"],
    "Tomato Basil Pasta": ["Pasta", "Tomatoes", "Basil", "Garlic"],
    "Sweet and Sour Chicken": ["Chicken Breasts", "Vinegar", "Sugar", "Ketchup"],
    "Baked Ziti": ["Ziti", "Marinara Sauce", "Ground Beef", "Mozzarella Cheese"],
    "Fried Chicken": ["Chicken Pieces", "Flour", "Salt", "Pepper"],
    "Beef and Broccoli": ["Beef", "Broccoli", "Soy Sauce", "Garlic"],
    "Chili Con Carne": ["Ground Beef", "Onions", "Tomatoes", "Kidney Beans"],
    "Chicken Noodle Soup": ["Chicken Breasts", "Noodles", "Carrots", "Celery"],
    "Beef Tacos": ["Ground Beef", "Tacos Shells", "Cheese", "Lettuce"],
    "French Toast": ["Bread", "Eggs", "Milk", "Sugar, Vanilla Extract"],
    "Tuna Salad Sandwich": ["Tuna", "Mayonnaise", "Bread", "Lettuce"],
    "Chicken Stir Fry": ["Chicken Breasts", "Vegetables", "Soy Sauce", "Garlic"],
    "Vegetable Soup": ["Vegetables", "Chicken Broth", "Salt", "Pepper"],
    "Beef Stew": ["Beef", "Potatoes", "Carrots", "Onions"],
    "Clam Chowder": ["Clams", "Potatoes", "Bacon", "Milk"],
    "Chicken Alfredo": ["Chicken Breasts", "Pasta", "Heavy Cream", "Parmesan Cheese"],
    "Turkey Sandwich": ["Turkey", "Bread", "Mayonnaise", "Lettuce"],
    "Lobster Bisque": ["Lobster", "Onions", "Flour", "Heavy Cream"],
    "Shepherd's Pie": ["Ground Beef", "Potatoes", "Carrots", "Peas"],
    "Shrimp Scampi": ["Shrimp", "Garlic", "White Wine", "Butter"],
    "BBQ Ribs": ["Pork Ribs", "BBQ Sauce", "Salt", "Pepper"],
    "Pork Chops": ["Pork Chops", "Olive Oil", "Salt", "Pepper"],
    "Steak Fajitas": ["Steak", "Bell Peppers", "Onions", "Flour Tortillas"],
    "Baked Salmon": ["Salmon", "Olive Oil", "Lemon", "Salt"],
    "Minestrone Soup": [
        "Vegetables",
        "Cannellini Beans",
        "Tomato Sauce",
        "Chicken Broth",
    ],
    "Beef and Noodles": ["Beef", "Noodles", "Carrots", "Onions"],
    "Turkey Chili": ["Turkey", "Kidney Beans", "Tomatoes", "Onions"],
    "Chicken Parmesan": [
        "Chicken Breasts",
        "Marinara Sauce",
        "Mozzarella Cheese",
        "Parmesan Cheese",
    ],
    "Beef Bourguignon": ["Beef", "Carrots", "Onions", "Red Wine"],
    "Cream of Mushroom Soup": ["Mushrooms", "Butter", "Flour", "Milk"],
}


words = [
    "Elephant",
    "Car",
    "Book",
    "Chair",
    "Mountain",
    "Ocean",
    "Sun",
    "Moon",
    "Stars",
    "Tree",
    "Flower",
    "Butterfly",
    "Rock",
    "River",
    "Island",
    "House",
    "Office",
    "School",
    "City",
    "Country",
    "Dog",
    "Cat",
    "Horse",
    "Giraffe",
    "Lion",
    "Tiger",
    "Elephant",
    "Plane",
    "Train",
    "Car",
    "Bicycle",
    "Telephone",
    "Computer",
    "Television",
    "Radio",
    "Music",
    "Art",
    "Painting",
    "Sculpture",
    "Museum",
    "Library",
    "Hospital",
    "Fire",
    "Police",
    "Movie",
    "Theater",
    "Circus",
    "Zoo",
    "Park",
    "Garden",
]

passkey = [
    random.choice(words),
    random.choice(words),
    random.choice(words),
    random.choice(words),
]

current_recipes = copy.deepcopy(recipes)

app = FastAPI(openapi_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def gen_new_challenge(recipes) -> dict:
    newrecipes = copy.deepcopy(recipes)
    used_keys = []
    while len(used_keys) < 4:
        n = random.sample(newrecipes.items(), 1)
        if n[0][0] not in used_keys:
            for key, val in n:
                keys_lower = key.lower().split(" ")
                values_lower = [x.lower() for x in val]
                for i, v in enumerate(values_lower):
                    if v in keys_lower:
                        newrecipes[key][i] = passkey[len(used_keys)]
                        used_keys.append(key)
                        break
    return newrecipes


def refresh_passkey():
    global passkey
    global current_recipes
    # global genLock


class BackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        global recipes
        global current_recipes
        global passkey
        global genLock
        while True:
            passkey = [
                random.choice(words),
                random.choice(words),
                random.choice(words),
                random.choice(words),
            ]
            logger.info(f"Generating new randoms -> {passkey}")
            # genLock.acquire()
            current_recipes = copy.deepcopy(gen_new_challenge(recipes))
            # genLock.release()
            time.sleep(refresh_time)


async def get_current_recipes():
    global genLock
    global current_recipes
    genLock.acquire()
    newrecipes = current_recipes
    genLock.release()
    return newrecipes


@app.on_event("startup")
async def startup_event():
    t = BackgroundTasks()
    t.start()


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/")


@app.exception_handler(ValidationError)
async def handler1(request: Request, exc: Exception):
    logger.error("ValidationError")
    return HTMLResponse(content="An error occured", status_code=503)


@app.exception_handler(RequestValidationError)
async def handler2(request: Request, exc: Exception):
    logger.error("RequestValidationError")
    logger.error(type(exc))
    return HTMLResponse(content="An error occured", status_code=503)


@app.exception_handler(Exception)
async def handler3(request: Request, exc: Exception):
    logger.error("Exception")
    logger.error(type(exc))
    return HTMLResponse(content="An error occured", status_code=503)


@app.get("/", response_class=HTMLResponse)
async def get_recipes(request: Request):
    # global #genLock
    # genLock.acquire()
    new_recipes = await get_current_recipes()
    # print(new_recipes)
    # genLock.release()
    # print(passkey)
    return templates.TemplateResponse(
        "index.html", {"request": request, "recipes": new_recipes, "query": None}
    )


@app.post("/", response_class=HTMLResponse)
async def check_recipes(
    request: Request,
    in1: str = Form(),
    in2: str = Form(),
    in3: str = Form(),
    in4: str = Form(),
):
    # global #genLock
    found = None

    new_recipes = await get_current_recipes()
    # genLock.release()
    if set([in1, in2, in3, in4]) == set(passkey):
        found = {"Flag": flag}
        logger.info("Someone found the flag! :)")
    else:
        for recipe in new_recipes:
            if set([in1, in2, in3, in4]) == set(recipes[recipe]):
                found = {recipe: recipes[recipe]}
                break

    return templates.TemplateResponse(
        "index.html", {"request": request, "recipes": new_recipes, "query": found}
    )
