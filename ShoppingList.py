# py
# Shopping List

import os
import re

# Files
ITEMS = "persistant_list.txt"
RECIPES = "MyBuiltRecipes.txt"


class ShoppingList:
    """
        API:
            display
            add_item
            delete_item(item)
            add_items_from_recipe_book(recipe_title)
    """
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
        The incoming string should be a quantity followed by an item name (optional),
        and we want to capitalize the item name. This will call a helper to either
        append a new line or increment an existing item's quantity.
        """
        if not incoming_item:
            return

        incoming_item = incoming_item.strip()
        _add_or_increment(incoming_item)
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
                    ingredients = _parse_ingredients(list_of_ingredients)
                    for ingr in ingredients:
                        ShoppingList.add_item(ingr)
                    added_any = True
                    break

        return added_any


def _parse_qty_and_name(item_str):
    """
    Parse a string that may start with an integer quantity followed by an item name.

    Returns a tuple: (quantity:int, name:str)
    If no leading quantity is present, quantity defaults to 1 and name is title-cased.
    """
    if not item_str:
        return 0, ""

    s = item_str.strip()
    m = re.match(r"^(\d+)\s+(.+)$", s)
    if m:
        qty = int(m.group(1))
        name = m.group(2).title().strip()
        return qty, name
    else:
        return 1, s.title().strip()


def _format_item_line(qty, name):
    """
    Format the line to write to the file.
    If qty <= 1, write just the name to preserve previous behavior.
    """
    if qty <= 1:
        return name
    return f"{qty} {name}"


def _add_or_increment(incoming_item):
    """
    Add the incoming item to the ITEMS file, or if an item with the same name
    already exists, increment its quantity.

    incoming_item may be a string like "2 apples" or "apples".
    """
    if not incoming_item:
        return

    incoming_qty, incoming_name = _parse_qty_and_name(incoming_item)

    # Read current items
    if not os.path.exists(ITEMS):
        # Ensure file exists before reading/writing
        open(ITEMS, "a", encoding="utf-8").close()

    with open(ITEMS, "r", encoding="utf-8") as file:
        lines = [ln.rstrip("\n") for ln in file.readlines()]

    normalized_target = incoming_name.casefold()
    updated = False

    for idx, line in enumerate(lines):
        if not line.strip():
            continue

        existing_qty, existing_name = _parse_qty_and_name(line)
        if existing_name.casefold() == normalized_target:
            new_qty = existing_qty + incoming_qty
            lines[idx] = _format_item_line(new_qty, existing_name)
            updated = True
            break

    if updated:
        # Write back modified list
        with open(ITEMS, "w", encoding="utf-8") as file:
            for ln in lines:
                file.write(ln + "\n")
            file.flush()
        return

    # Not found: append as new line
    new_line = _format_item_line(incoming_qty, incoming_name)
    with open(ITEMS, "a", encoding="utf-8") as file:
        file.write(new_line + "\n")
        file.flush()


def _parse_ingredients(list_of_ingredients):
    if not list_of_ingredients:
        return []
    return [i.strip() for i in list_of_ingredients.split(";") if i.strip()]