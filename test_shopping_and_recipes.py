import io
import os
import random

import pytest

import ShoppingList
import Recipes


# ------------------------
# Fixtures
# ------------------------
@pytest.fixture
def tmp_items_file(tmp_path, monkeypatch):
    path = tmp_path / "items.txt"
    # override module-level constant so tests don't touch real file
    monkeypatch.setattr(ShoppingList, "ITEMS", str(path))
    return path


@pytest.fixture
def tmp_recipes_file(tmp_path, monkeypatch):
    path = tmp_path / "recipes.txt"
    monkeypatch.setattr(ShoppingList, "RECIPES", str(path))
    monkeypatch.setattr(Recipes, "MY_FILE", str(path))
    return path


# Helper to find index of a token in a list of lines (case-insensitive)
def _index_of_token(lines, token):
    token = token.lower()
    for idx, line in enumerate(lines):
        if token in line.lower():
            return idx
    return -1


# ------------------------
# ShoppingList tests
# ------------------------
def test_parse_qty_and_name_empty():
    qty, name = ShoppingList._parse_qty_and_name("")
    assert qty == 0
    assert name == ""


def test_parse_qty_and_name_with_quantity():
    qty, name = ShoppingList._parse_qty_and_name("3 apples")
    assert qty == 3
    assert name == "Apples"


def test_parse_qty_and_name_without_quantity():
    qty, name = ShoppingList._parse_qty_and_name("banana")
    assert qty == 1
    assert name == "Banana"


def test_format_item_line():
    assert ShoppingList._format_item_line(1, "Apple") == "Apple"
    assert ShoppingList._format_item_line(4, "Apple") == "4 Apple"


def test_add_item_new_and_increment(tmp_items_file):
    # call the class static method (ShoppingList is a module; ShoppingList.ShoppingList is the class)
    ShoppingList.ShoppingList.add_item("2 apple")
    with open(str(tmp_items_file), "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    assert any("2 apple" == l.lower() for l in lines)

    # increment existing
    ShoppingList.ShoppingList.add_item("3 apple")
    with open(str(tmp_items_file), "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    assert any(l.lower().startswith("5 ") and "apple" in l.lower() for l in lines)

    # add item without explicit qty -> default 1
    ShoppingList.ShoppingList.add_item("banana")
    with open(str(tmp_items_file), "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines()]
    assert any(l.lower() == "banana" for l in lines)


def test_delete_item_removes_matching_lines(tmp_items_file):
    content = "2 Apple\nBanana\n3 Rice\n"
    tmp_items_file.write_text(content, encoding="utf-8")
    ShoppingList.ShoppingList.delete_item("apple")
    remaining = tmp_items_file.read_text(encoding="utf-8").splitlines()
    assert not any("apple" in l.lower() for l in remaining)
    assert any("banana" in l.lower() for l in remaining)
    assert any("rice" in l.lower() for l in remaining)


def test_add_items_from_recipe_book_appends_ingredients(
    tmp_items_file, tmp_recipes_file
):
    # prepare recipe file
    tmp_recipes_file.write_text("Pancakes;2 milk;3 eggs;flour\n", encoding="utf-8")
    # ensure items file is empty/nonexistent initially
    if tmp_items_file.exists():
        tmp_items_file.unlink()

    added = ShoppingList.ShoppingList.add_items_from_recipe_book("Pancakes")
    assert added is True

    lines = tmp_items_file.read_text(encoding="utf-8").splitlines()
    assert any("milk" in l.lower() for l in lines)
    assert any("eggs" in l.lower() for l in lines)
    assert any("flour" in l.lower() for l in lines)


def test_organize_list_order_and_write_back(tmp_items_file):
    # Create items in mixed order (preserve the casing as test wrote it)
    tmp_items_file.write_text(
        "1 Milk\n2 rice\n3 apple\n4 Ice Cream\n", encoding="utf-8"
    )
    ordered = ShoppingList.organize_list(write_back=True)

    # use token-based lookup to avoid exact-casing assumptions
    idx_apple = _index_of_token(ordered, "apple")
    idx_rice = _index_of_token(ordered, "rice")
    idx_milk = _index_of_token(ordered, "milk")
    idx_icecream = _index_of_token(ordered, "ice cream")

    assert idx_apple != -1 and idx_rice != -1 and idx_milk != -1 and idx_icecream != -1
    assert idx_apple < idx_rice < idx_milk < idx_icecream

    # File should have been overwritten in the same order (without headers)
    file_lines = tmp_items_file.read_text(encoding="utf-8").splitlines()
    assert [l for l in file_lines] == ordered


def test__parse_ingredients_empty_or_values():
    assert ShoppingList._parse_ingredients("") == []
    assert ShoppingList._parse_ingredients("a;b;;c") == ["a", "b", "c"]


def test__match_category_exact_substring_word():
    lookup = ShoppingList._build_category_lookup()
    # exact
    assert ShoppingList._match_category("apple", lookup) == "Produce"
    # substring (e.g., 'sweet potato' token exists, use substring)
    assert ShoppingList._match_category("sweet potatoes", lookup) == "Produce"
    # word-level (name with extra words)
    assert ShoppingList._match_category("bacon bits", lookup) == "Fridge"
    # note: "unicorn" contains "corn" which is in the Frozen tokens -> Frozen expected
    assert ShoppingList._match_category("unicorn", lookup) == "Frozen"


# ------------------------
# Recipes tests
# ------------------------
def test_read_file_for_titles_and_get_ingredients(tmp_recipes_file):
    content = "Pancakes;2 milk;3 eggs;flour\n\nOmelette;2 eggs;1 cheese\n"
    tmp_recipes_file.write_text(content, encoding="utf-8")

    titles = Recipes._read_file_for_titles()
    assert "Pancakes" in titles
    assert "Omelette" in titles

    ingredients = Recipes.Recipes.get_ingredients("pancakes")
    assert "2 milk" in ingredients
    assert "3 eggs" in ingredients
    assert "flour" in ingredients

    assert Recipes.Recipes.get_ingredients("") == []
    assert Recipes.Recipes.get_ingredients("nope") == []


def test_add_and_delete_recipe(tmp_recipes_file):
    # start clean
    if tmp_recipes_file.exists():
        tmp_recipes_file.unlink()
    ok = Recipes.Recipes.add_recipe("french toast", ["2 egg", ("1", "milk"), "bread"])
    assert ok is True
    data = tmp_recipes_file.read_text(encoding="utf-8").splitlines()
    assert any(line.lower().startswith("french toast;") for line in data)

    Recipes.Recipes.add_recipe("salad", ["lettuce", "1 tomato"])
    removed = Recipes.Recipes.delete_recipe("french toast")
    assert removed is True
    remaining = tmp_recipes_file.read_text(encoding="utf-8").splitlines()
    assert not any(line.casefold().startswith("french toast;") for line in remaining)


def test_propose_rand_title_returns_valid_title(tmp_recipes_file, monkeypatch):
    tmp_recipes_file.write_text("A;1 x\nB;2 y\n", encoding="utf-8")
    titles = Recipes._read_file_for_titles()
    monkeypatch.setattr(random, "choice", lambda seq: seq[0])
    t = Recipes.Recipes.propose_rand_title()
    assert t in titles
