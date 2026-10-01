# python
# Recipes

import random

# Files
MY_FILE = "MyBuiltRecipes.txt"

# Global Recipes buffer
LIST_OF_INGREDIENTS_BUFFER = []


def _read_file_for_titles():
    list_of_recipes = []
    try:
        with open(MY_FILE, "r") as file:
            for line in file:
                recipe = line.strip()
                if not recipe:
                    continue
                recipe_title, _, _ = recipe.partition(";")
                list_of_recipes.append(recipe_title)
    except FileNotFoundError:
        return []
    return list_of_recipes


class Recipes:
    """
    API:
        display()
        get_ingredients(title)
        add_recipe(title, items)
        delete_recipe(title)
    """

    @staticmethod
    def display():
        list_of_recipes = _read_file_for_titles()

        for i in list_of_recipes:
            print(f"{i}")
        return list_of_recipes

    @staticmethod
    def get_ingredients(title):
        """
        Return the list of ingredients (strings) for a recipe title.
        Matching is case-insensitive. If not found, returns an empty list.
        File format: Title;ingredient1;ingredient2;...
        """
        if not title:
            return []
        target = title.strip().casefold()
        ingredients = []
        try:
            with open(MY_FILE, "r") as file:
                for line in file:
                    recipe = line.strip()
                    if not recipe:
                        continue
                    recipe_title, _, list_of_ingredients = recipe.partition(";")
                    if recipe_title.strip().casefold() == target:
                        if list_of_ingredients:
                            ingredients = [
                                i.strip()
                                for i in list_of_ingredients.split(";")
                                if i.strip()
                            ]
                        break
        except FileNotFoundError:
            return []
        return ingredients

    @staticmethod
    def add_recipe(title, items):
        """
        Add a recipe to the file.

        - title: string
        - items: iterable of strings like "2 Apple" or tuples (qty, name)

        Returns True on success, False on failure.
        """
        if not title or not items:
            return False

        def _format_item(it):
            if isinstance(it, tuple) and len(it) >= 2:
                qty, name = int(it[0]), str(it[1]).strip()
                return f"{qty} {name}"
            s = str(it).strip()
            parts = s.split(None, 1)
            if len(parts) == 1:
                return f"1 {parts[0]}"
            return s

        normalized_items = [_format_item(it) for it in items if str(it).strip()]
        if not normalized_items:
            return False

        line = title.strip().capitalize() + ";" + ";".join(normalized_items)
        try:
            with open(MY_FILE, "a") as file:
                file.write(line + "\n")
        except Exception:
            return False
        return True

    @staticmethod
    def delete_recipe(title):
        """
        Remove a recipe by title. Returns True if removed.
        """
        if not title:
            return False

        target = title.strip().casefold()
        try:
            with open(MY_FILE, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return False

        removed = False
        try:
            with open(MY_FILE, "w") as file:
                for line in lines:
                    recipe_title, _, rest = line.partition(";")
                    if recipe_title.strip().casefold() == target:
                        removed = True
                        continue
                    file.write(line)
        except Exception:
            return False
        return removed

    @staticmethod
    def propose_rand_title():
        list_of_titles = _read_file_for_titles()
        random_title = random.choice(list_of_titles)
        return random_title