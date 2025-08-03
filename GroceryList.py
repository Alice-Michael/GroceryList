# py
# Main app invoking the whole project

# Project includes
import Recipes
import ShoppingList
from main import MainApp
# kivy includes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager


def display_menu():
     print("\nShopping List Menu:")
     print("1. Add item")
     print("2. Delete item")
     print("3. View list")
     print("4. Recipes Menu")
     print("5. Add ingredients from recipe")
     print("9. Exit")
     return


def shopping_list():
    while True:
        display_menu()   

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            ShoppingList.add_item_to_list()
        elif choice == '2':
            ShoppingList.delete_item_from_list()
        elif choice == '3':
            ShoppingList.display_list()
        elif choice == '4':
            Recipes.recipes_options()
        elif choice == '5':
            ShoppingList.add_items_from_recipe_book()
        elif choice == '9':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
    return

# Main flow
#shopping_list()
MainApp().run()