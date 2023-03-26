# importing the modules
import requests
from bs4 import BeautifulSoup
from time import sleep
import numpy as np


def find_different_items(*arrays):
    """
    Given multiple arrays, returns a set of all items that are different between the arrays.
    """
    different_items = set()
    for array in arrays:
        different_items.update(set(array) - set(different_items))
    return different_items


def find_different_items_nested(*arrays):
    """
    Given multiple arrays (which may be nested), returns a set of all items that are different between the arrays.
    """
    flattened_arrays = []
    for array in arrays:
        if isinstance(array, list):
            flattened_arrays.extend(find_different_items_nested(*array))
        else:
            flattened_arrays.append(array)
    different_items = set()
    for item in flattened_arrays:
        if item not in different_items:
            different_items.add(item)
        else:
            different_items.remove(item)
    return different_items


def parse_page() -> dict:
    # providing url
    url = "http://127.0.0.1:8000"

    # creating requests object
    html = requests.get(url).content

    # creating soup object
    data = BeautifulSoup(html, "html.parser")

    # finding parent <ul> tag
    recipes = data.find_all("div", {"class": "recipe"})[1:]
    rcp = {}
    for recipe in recipes:
        tag = recipe.find_all("h2")[0].text.strip()
        ingredients = recipe.find_all("li")[0:4]
        ingredients = [x.text.strip() for x in ingredients]
        rcp[tag] = ingredients
    return rcp


def train(nb_of_trains=20):
    weird_words = open("weird_words.txt", "w")
    recipes_array = []
    for _ in range(nb_of_trains):
        recipes_array.append(parse_page())
        sleep(5)

    comparing_array = []
    for recipes in recipes_array:
        ingred = []
        for val in recipes.values():
            for v in val:
                ingred.append(v)
        comparing_array.append(list(dict.fromkeys(ingred)))

    items = find_different_items_nested(comparing_array)
    # items {'Book', 'Red Wine', 'Romaine Lettuce', 'Celery', 'Sugar, Vanilla Extract', 'Tomato', 'BBQ Sauce', 'Steak', 'Tomato Sauce', 'Parmesan Cheese', 'Car', 'Lettuce', 'Marinara Sauce', 'Flour', 'White Wine', 'Ground Beef', 'Basil', 'Carrots', 'Vinegar', 'Sun', 'Pancetta', 'Tacos Shells', 'Mountain', 'Salmon', 'Tomatoes', 'Olive Oil', 'Clams', 'Telephone', 'Cheese', 'Heavy Cream', 'Beef', 'Bacon', 'Shrimp', 'Garlic', 'Plane', 'Kidney Beans', 'Milk', 'Chicken Pieces', 'Pasta', 'Mayonnaise', 'Tree', 'Croutons', 'Chicken Broth', 'Cannellini Beans', 'Salt', 'Movie', 'Peas', 'Bicycle', 'Butter', 'Flour Tortillas', 'Music', 'Mushrooms', 'Spaghetti', 'Art', 'Bell Peppers', 'Macaroni', 'Eggs', 'Broccoli', 'Onions', 'Chicken Breasts', 'Soy Sauce', 'Pepper', 'City', 'Onion', 'Pork Ribs', 'Caesar Dressing', 'Noodles', 'Vegetables', 'Mozzarella Cheese', 'Lemon', 'Bread', 'Chair', 'Lobster', 'Potatoes', 'Pork Chops', 'Sugar', 'Ocean', 'Ketchup'}
    print(items)
    counter_saver = {}
    for e in list(items):
        counter = 0
        for j in comparing_array:
            counter += j.count(e)
        counter_saver[e] = counter

    for key, val in counter_saver.items():
        if val < nb_of_trains - 1:
            weird_words.write(f"{key}\n")
    weird_words.close()


def get_flag(keywords):
    # providing url
    url = "http://127.0.0.1:8000"

    data = {
        "in1": keywords[0],
        "in2": keywords[1],
        "in3": keywords[2],
        "in4": keywords[3],
    }
    # creating requests object
    html = requests.post(url, data=data).content
    # creating soup object
    page = BeautifulSoup(html, "html.parser")

    # finding parent <ul> tag
    div = page.find_all("div", {"class": "queryrecipe"})[0]
    if "not" not in div.find_all("h1")[0].text.strip().lower():
        flag = div.find_all("li")
        flag = [x.text.strip() for x in flag]
        print(f"Here is your flag: {''.join(flag)}")
    else:
        print("Failed try again!")


def exploit():
    weird_words = open("weird_words.txt", "r").readlines()
    weird_words = [x.rstrip() for x in weird_words]
    weird_words = np.array(weird_words)
    keywords = []
    while len(keywords) < 4:
        sleep(1)
        keywords = []
        pg = parse_page()
        for key, val in pg.items():
            find_commons = np.intersect1d(weird_words, np.array(val))
            if find_commons.size > 0:
                keywords.append(find_commons[0])
    print(f"Found key words! {keywords}\nRetrieving the flag!")
    get_flag(keywords)


# Train for x number of sessions to look for non food related words and write them to a file
# train(50)

# Sort the file and remove non food related words
input(
    "Have a look at the words and remove potential shitty words! [Enter to continue exploitation]"
)

# Use the non food related words to spot changing words and therefore get the flag
exploit()
