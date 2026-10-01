# py
# Shopping List

import os
import re
from typing import Dict, List, Set, Tuple

# Files
ITEMS = "persistant_list.txt"
RECIPES = "MyBuiltRecipes.txt"

_needs_organizing = True


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
        global _needs_organizing

        if _needs_organizing:
            lines = _organize_list(write_back=False)
            _needs_organizing = False
            if lines:
                print("Shopping list:")
                for l in lines:
                    print(l)
                return lines

        list_of_items = []
        if os.path.exists(ITEMS):
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
        Remove any lines from the ITEMS file that contain the provided incoming_item,
        and mark the list as needing organization.
        """
        global _needs_organizing

        if not incoming_item:
            return

        target = incoming_item.strip().lower()

        # Read current items
        if not os.path.exists(ITEMS):
            return

        with open(ITEMS, "r", encoding="utf-8") as file:
            temp_items = file.readlines()

        # Write back only lines that do NOT contain the target string
        with open(ITEMS, "w", encoding="utf-8") as file:
            for line in temp_items:
                if target not in line.lower():
                    file.write(line)

        _needs_organizing = True
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

        with open(RECIPES, "r", encoding="utf-8") as file:
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


# ------------------------
# Internal helpers (module-level)
# ------------------------


def _parse_qty_and_name(item_str: str) -> Tuple[int, str]:
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


def _format_item_line(qty: int, name: str) -> str:
    """
    Format the line to write to the file.
    If qty <= 1, write just the name to preserve previous behavior.
    """
    if qty <= 1:
        return name
    return f"{qty} {name}"


def _add_or_increment(incoming_item: str) -> None:
    """
    Add the incoming item to the ITEMS file, or if an item with the same name
    already exists, increment its quantity.
    """
    global _needs_organizing

    if not incoming_item:
        return

    incoming_qty, incoming_name = _parse_qty_and_name(incoming_item)

    # Ensure file exists
    if not os.path.exists(ITEMS):
        open(ITEMS, "a").close()

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
        _needs_organizing = True
        return

    # Not found: append as new line
    new_line = _format_item_line(incoming_qty, incoming_name)
    with open(ITEMS, "a", encoding="utf-8") as file:
        file.write(new_line + "\n")
        file.flush()
    _needs_organizing = True


def _parse_ingredients(list_of_ingredients: str) -> List[str]:
    if not list_of_ingredients:
        return []
    return [i.strip() for i in list_of_ingredients.split(";") if i.strip()]


# ------------------------
# Organization helpers
# ------------------------


def _build_category_lookup() -> Dict[str, Set[str]]:
    """
    Return a mapping from category name to a set of canonical item strings to match against.
    Extend these sets as needed. Stored lower-cased for case-insensitive matching.
    """
    return {
        "Produce": {
            "apple",
            "banana",
            "orange",
            "lettuce",
            "spinach",
            "tomato",
            "potato",
            "onion",
            "garlic",
            "carrot",
            "cucumber",
            "pepper",
            "avocado",
            "salad",
            "sweet potato",
            "broccoli",
        },
        "Shelf-stable": {
            "rice",
            "pasta",
            "bread",
            "flour",
            "sugar",
            "cereal",
            "beans",
            "lentils",
            "oil",
            "spices",
            "salt",
            "coffee",
            "tea",
        },
        "Fridge": {
            "milk",
            "cheese",
            "butter",
            "yogurt",
            "eggs",
            "cream",
            "deli",
            "ham",
            "bacon",
            "beefnt",
        },
        "Frozen": {
            "peas",
            "corn",
            "ice cream",
            "frozen pizza",
            "frozen vegetables",
            "shrimp",
            "chicken",
            "hamburger patties",
        },
    }


def _match_category(name: str, lookup: Dict[str, Set[str]]) -> str:
    """
    Determine the category for 'name' using the following strategy:
      1. Exact canonical match (case-insensitive)
      2. Substring match (any lookup token appears in name)
      3. Word-level match (any word from name equals a lookup token)
    Returns category name or 'Other' when no match is found.
    """
    n = name.casefold()
    # 1. exact
    for cat, tokens in lookup.items():
        if n in tokens:
            return cat

    # 2. substring
    for cat, tokens in lookup.items():
        for token in tokens:
            if token in n or n in token:
                return cat

    # 3. word-level
    words = re.findall(r"\w+", n)
    for cat, tokens in lookup.items():
        if any(w in tokens for w in words):
            return cat

    return "Other"


def _organize_list(write_back: bool = False) -> List[str]:
    """
    Read ITEMS, organize lines into the order:
      Produce, Shelf-stable, Fridge, Frozen, Other
    Returns a list of output lines (including section headers).
    If write_back is True, overwrite ITEMS with the organized list (without headers)
    and also return the lines with headers for display.
    """
    if not os.path.exists(ITEMS):
        return []

    lookup = _build_category_lookup()
    ordered_categories = ["Produce", "Shelf-stable", "Fridge", "Frozen", "Other"]
    buckets: Dict[str, List[str]] = {c: [] for c in ordered_categories}

    with open(ITEMS, "r", encoding="utf-8") as file:
        for raw in file:
            line = raw.strip()
            if not line:
                continue
            _, name = _parse_qty_and_name(line)
            category = _match_category(name, lookup)
            buckets[category].append(line)

    flattened: List[str] = []
    for cat in ordered_categories:
        flattened.extend(buckets.get(cat, []))

    # Optionally write back items in category order without headers (preserves file format)
    if write_back:
        with open(ITEMS, "w", encoding="utf-8") as file:
            for ln in flattened:
                file.write(ln + "\n")
            file.flush()

    return flattened


def organize_list(write_back: bool = False) -> List[str]:
    """
    Public wrapper to organize the shopping list. Returns lines suitable for display
    (category-ordered, without headers). If write_back=True the ITEMS file will be
    rewritten in the organized order. Calling this will also mark the list as organized.
    """
    global _needs_organizing
    lines = _organize_list(write_back=write_back)
    _needs_organizing = False
    return lines
