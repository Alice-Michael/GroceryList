# py
# Shopping List

import os
import re

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


class ShoppingList:
    def display():
        list_of_items = []
        with open(ITEMS, "r", encoding="utf-8") as file:
            for line in file:
                list_of_items.append(line.strip())

        print("Shopping list:")
        for i in list_of_items:
            print(f"{i}")
        return list_of_items

    def add_item(incoming_item):
        """
        The incoming string should be a quantity followed by an item name, and
        we want to capitalize the item name.
        """
        if not incoming_item:
            return

        incoming_item = incoming_item.strip()

        # If leading numeric quantity followed by space, preserve it and title-case the rest.
        m = re.match(r"^(\d+\s+)(.+)$", incoming_item)
        if m:
            qty = m.group(1).strip()
            rest = m.group(2).title()
            normalized = f"{qty} {rest}"
        else:
            normalized = incoming_item.title()

        with open(ITEMS, "a", encoding="utf-8") as file:
            file.write(normalized + "\n")
            file.flush()
        return

    def delete_item(incoming_item):
        """
        Remove any lines from the ITEMS file that contain the provided incoming_item.
        """
        if not incoming_item:
            return

        target = incoming_item.strip().lower()

        # Read current items
        with open(ITEMS, "r") as file:
            temp_items = file.readlines()

        # Write back only lines that do NOT contain the target string
        with open(ITEMS, "w") as file:
            for line in temp_items:
                if target not in line.lower():
                    file.write(line)
        return

    def _parse_ingredients(list_of_ingredients):
        if not list_of_ingredients:
            return []
        return [i.strip() for i in list_of_ingredients.split(";") if i.strip()]

    def add_items_from_recipe_book(self, find_recipe=None):
        """
        Find a recipe in RECIPES and append its ingredients to the shopping list.
        If find_recipe is None, prompt the user (maintains CLI compatibility).
        Recipe file format assumed: "Title;ingredient1;ingredient2;..."
        """
        if find_recipe is None:
            find_recipe = input("What recipe do you want to add: ").strip()

        target_title = find_recipe.capitalize()

        with open(RECIPES, "r") as file:
            for line in file:
                recipe = line.strip()
                recipe_title, _, list_of_ingredients = recipe.partition(";")
                if recipe_title == target_title:
                    ingredients = self._parse_ingredients(list_of_ingredients)
                    for ingr in ingredients:
                        # Each parsed ingredient may already include a quantity; normalize via add_item
                        self.add_item(ingr)
                    break
        return