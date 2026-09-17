# py
# Shopping List

import os
import re

# Files
ITEMS = "persistant_list.txt"
RECIPES = "MyBuiltRecipes.txt"


class ShoppingList:
    @staticmethod
    def display():
        list_of_items = []
        with open(ITEMS, "r", encoding="utf-8") as file:
            for line in file:
                list_of_items.append(line.strip())

        print("Shopping list:")
        for i in list_of_items:
            print(f"{i}")
        return list_of_items

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def _parse_ingredients(list_of_ingredients):
        if not list_of_ingredients:
            return []
        return [i.strip() for i in list_of_ingredients.split(";") if i.strip()]

    @staticmethod
    def add_items_from_recipe_book(find_recipe=None):
        """
        Find a recipe in RECIPES and append its ingredients to the shopping list.
        If find_recipe is None, prompt the user (maintains CLI compatibility).
        Recipe file format assumed: "Title;ingredient1;ingredient2;..."
        """
        if find_recipe is None:
            find_recipe = input("What recipe do you want to add: ").strip()

        if not find_recipe:
            return False

        if not os.path.exists(RECIPES):
            print(f"Recipe file '{RECIPES}' not found.")
            return False

        target = find_recipe.strip().casefold()
        added_any = False

        with open(RECIPES, "r") as file:
            for line in file:
                recipe = line.strip()
                if not recipe:
                    continue
                recipe_title, _, list_of_ingredients = recipe.partition(";")
                if recipe_title.strip().casefold() == target:
                    ingredients = ShoppingList._parse_ingredients(list_of_ingredients)
                    for ingr in ingredients:
                        ShoppingList.add_item(ingr)
                    added_any = True
                    break

        return added_any