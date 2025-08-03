# python
# Recipes

# kivy includes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager


# Files
MY_FILE = "MyBuiltRecipes.txt"

# Global Recipes buffer
LIST_OF_INGREDIENTS_BUFFER = []

def recipes_menu():
    print("1. Show recipes")
    print("2. Add recipe")
    print("3. Delete recipe")
    print("9. Return to main menu")
    return


def recipes_options():
    recipes_options = True

    while recipes_options:
        recipes_menu()

        choice = input("Enter your choice by number: ")
    
        if choice == '1':
            display_recipes()
        elif choice == '2':
            add_recipe_to_list()
        elif choice == '3':
            remove_recipe_from_list()
        elif choice == '9':
            print("Returning to main menu")
            recipes_options = False
        else:
            print("Invalid choice")
            recipes_options()
    return


def display_recipes():
    # Show a list of recipes
    list_of_recipes = []
    with open(MY_FILE, "r") as file:
        for line in file:
            recipe = line.strip()
            recipe_title, _, _ = recipe.partition(';')
            list_of_recipes.append(recipe_title)
    for i in list_of_recipes:
        print(f"{i}")
    return


def write_recipe_to_file(title):
    line_to_write = title.capitalize() + ";" + ";".join(LIST_OF_INGREDIENTS_BUFFER)
    with open(MY_FILE, "a") as file:
        file.write(line_to_write + '\n')
    return


def get_item_for_recipe():
    adding = True

    while adding:
        item_for_recipe = input("Enter item: ")
        if not (2 <= len(item_for_recipe) <= 100):    
            print("item length out of range.")
            continue
        else:
            adjusting_size = True
            while adjusting_size == True:
                num_items = input("Enter how many: ")
                if (int(num_items) > 20):
                    response = input("You entered a large quantity, is {num_items} accurate? (y/n)")
                    if response == 'y':
                        print(f"adding {num_items} of {item_for_recipe} to recipe")
                        adjusting_size = False
                else:
                    print(f"Adding {num_items} of {item_for_recipe} to recipe")
                    adjusting_size = False

        still_adding = input("More items to add? (y/n): ")
        if still_adding != 'y':
            adding = False

        LIST_OF_INGREDIENTS_BUFFER.append(num_items + ' ' + item_for_recipe)

    return


def add_recipe_to_list():
    LIST_OF_INGREDIENTS_BUFFER.clear()
    adding = True
    title = input(f"Enter the name of the recipe: ")

    if not (3 <= len(title) <= 100):
        print(f"Title length out of range.")
        return

    get_item_for_recipe()

    write_recipe_to_file(title)
    return


def remove_recipe_from_list():
    recipe_to_delete = input("What recipe do you want to remove: ")
    not_deleting_line = True

    with open(MY_FILE, "r") as file:
        temp_recipes = file.readlines()

    with open(MY_FILE, "w") as file:
        for line in temp_recipes:
            recipe_title, _, _ = line.partition(';')
            if recipe_title == recipe_to_delete.capitalize():
                not_deleting_line = False
                print(f"Removing {recipe_title}")
            if not_deleting_line:
                file.write(line)
            not_deleting_line = True
    return

####################################################################################
#                                  APP SPECIFIC                                    #
####################################################################################
def display_list_app():
    list_of_recipes = []
    with open(MY_FILE, "r") as file:
        for line in file:
            recipe = line.strip()
            recipe_title, _, _ = recipe.partition(';')
            list_of_recipes.append(recipe_title)
    for i in list_of_recipes:
        print(f"{i}")
    return list_of_recipes
