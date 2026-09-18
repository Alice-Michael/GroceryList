# python
# Recipes

# Files
MY_FILE = "MyBuiltRecipes.txt"

# Global Recipes buffer
LIST_OF_INGREDIENTS_BUFFER = []


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
        list_of_recipes = []
        try:
            with open(MY_FILE, "r") as file:
                for line in file:
                    recipe = line.strip()
                    if not recipe:
                        continue
                    recipe_title, _, _ = recipe.partition(';')
                    list_of_recipes.append(recipe_title)
        except FileNotFoundError:
            return []
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
                    recipe_title, _, list_of_ingredients = recipe.partition(';')
                    if recipe_title.strip().casefold() == target:
                        if list_of_ingredients:
                            ingredients = [i.strip() for i in list_of_ingredients.split(';') if i.strip()]
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
                    recipe_title, _, rest = line.partition(';')
                    if recipe_title.strip().casefold() == target:
                        removed = True
                        continue
                    file.write(line)
        except Exception:
            return False
        return removed


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
    list_of_recipes = Recipes.display()
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
                    response = input(f"You entered a large quantity, is {num_items} accurate? (y/n)")
                    if response == 'y':
                        print(f"adding {num_items} of {item_for_recipe} to recipe")
                        adjusting_size = False
                else:
                    print(f"Adding {num_items} of {item_for_recipe}")
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
