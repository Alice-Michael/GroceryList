# py
# Shopping List

import os

# kivy includes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager


# Files
ITEMS = "persistant_list.txt"
RECIPES = "MyBuiltRecipes.txt"

# Global List Buffer
INGREDIENTS_BUFFER = []

def display_list():
    print("Shopping list:")
    with open(ITEMS, "r") as file:
        for line in file:
            print(f"{line.strip()}")
    return


def add_item_to_list():
    item = input("Enter the item to add: ")
    with open(ITEMS, "a") as file:
        file.write(item.capitalize() + '\n')
        file.flush()
    return

def delete_item_from_list():
    item_to_delete = input("What item do you want to remove from the shopping list: ")
    
    with open(ITEMS, "r") as file:
        temp_items = file.readlines()

    with open(ITEMS, "w") as file:
        for line in temp_items:
            if item_to_delete.capitalize() not in line:
                file.write(line)
    return


def parse_ingredients(list_of_ingredients):
    print(f"in parse function")
    items = list_of_ingredients.split(';')
    for i in items:
        INGREDIENTS_BUFFER.append(i)

    return


def write_items_from_parsed_recipe():
    with open(ITEMS, "a") as file:
        for i in INGREDIENTS_BUFFER:
            file.write(i + '\n')
    return


def add_items_from_recipe_book():
    INGREDIENTS_BUFFER.clear()

    find_recipe = input("What recipe do you want to add: ")

    with open (RECIPES, "r") as file:
        for line in file:
            recipe = line.strip()
            recipe_title, _, list_of_ingredients = recipe.partition(';')
            print(f"current recipe: {recipe_title}")
            if recipe_title == find_recipe.capitalize():
                print(f"found {recipe_title}")
                parse_ingredients(list_of_ingredients)
                break

    write_items_from_parsed_recipe()
    return

####################################################################################
#                                  APP SPECIFIC                                    #
####################################################################################
def display_list_app():
    list_of_items = []
    with open(ITEMS, "r") as file:
        for line in file:
            list_of_items.append(line.strip())
        
    print("Shopping list:")
    for i in list_of_items:
        print(f"{i}")
    return list_of_items
       
def add_item_to_list_app(incoming_item):
    with open(ITEMS, "a") as file:
        file.write(incoming_item.capitalize() + '\n')
        # force the write to happen now.
        file.flush()
    return

def delete_item_from_list_app(incoming_item):
    """
    Remove any lines from the ITEMS file that contain the provided incoming_item.
    Matches the same capitalization approach used by add_item_to_list_app.
    """
    if not incoming_item:
        return

    target = incoming_item.capitalize()

    # Read current items
    with open(ITEMS, "r") as file:
        temp_items = file.readlines()

    # Write back only lines that do NOT contain the target string
    with open(ITEMS, "w") as file:
        for line in temp_items:
            if target not in line:
                file.write(line)
    return