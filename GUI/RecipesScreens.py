# kivy imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivy.metrics import dp

# App imports
from CORE.Recipes import Recipes
from CORE.ShoppingList import ShoppingList
from GUI.BaseScreen import BaseScreen

recipes_menu_options = [
    "Show Recipes",
    "Add recipe",
    "Delete recipe",
    "Propose Recipe to cook",
    "Back",
]


class RecipesMenu(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _populate_detail_screen(self):
        self.rand_recipe_title = Recipes.propose_rand_title()
        # Try to get existing detail screen; if missing, create, init and register it dynamically.
        try:
            detail_screen = self.sm.get_screen("RecipeDetail")
        except Exception:
            # create, initialize and add the screen
            detail_screen = RecipeDetailScreen(name="RecipeDetail")
            detail_screen.initUI(self.sm)
            self.sm.add_widget(detail_screen)
        detail_screen.display_recipe(self.rand_recipe_title)

    def initUI(self, screen_manager_handle):
        # Use base helper to create layout (no Back button for main menu)
        col1, _ = self.setup_screen(
            screen_manager_handle,
            title_text="Recipes Menu",
            title_size="20",
            back_target=None,
            include_back=False,
        )

        # Add menu options
        for opt in recipes_menu_options:
            btn = Button(
                text=f"{opt}",
                size_hint=(1, 0.12),
                pos_hint={"center_x": 0.5},
            )
            btn.bind(on_press=self.button_click)
            col1.add_widget(btn)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        elif option_text == "Show Recipes":
            self.sm.current = "ViewRecipesList"
        elif option_text == "Add recipe":
            self.sm.current = "AddRecipeScreen"
        elif option_text == "Propose Recipe to cook":
            self._populate_detail_screen()
            self.sm.current = "RecipeDetail"
        elif option_text == "Delete recipe":
            self.sm.current = "DelRecipeScreen"
        else:
            pass


class RecipeViewList(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # create layout and back button via BaseScreen helper
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Recipes",
            title_size="20",
            back_target="RecipesMenu",
        )

        list_of_recipes = Recipes.display()

        self.populate_list(col1, list_of_recipes)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
            return

        recipe_title = option_text.strip()

        # Try to get existing detail screen; if missing, create, init and register it dynamically.
        try:
            detail_screen = self.sm.get_screen("RecipeDetail")
        except Exception:
            # create, initialize and add the screen
            detail_screen = RecipeDetailScreen(name="RecipeDetail")
            detail_screen.initUI(self.sm)
            self.sm.add_widget(detail_screen)

        # populate and navigate
        detail_screen.display_recipe(recipe_title)
        self.sm.current = "RecipeDetail"


class AddRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pending_items = []
        self._items_container = None
        self._qty_input = None
        self._item_input = None
        self._title_input = None
        self._status_label = None

    def initUI(self, screen_manager_handle):
        # setup base layout with back target
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Add saved recipe",
            title_size="20",
            back_target="RecipesMenu",
        )

        # Title input
        self._title_input = TextInput(hint_text="Recipe title", size_hint=(1, 0.1))
        col1.add_widget(self._title_input)

        # Row to enter qty and item and add to pending list
        row = BoxLayout(size_hint=(1, 0.1))
        self._qty_input = TextInput(
            hint_text="Qty", size_hint=(0.2, 1), input_filter="int"
        )
        self._item_input = TextInput(hint_text="Item name", size_hint=(0.6, 1))
        add_btn = Button(text="Add item", size_hint=(0.2, 1))
        add_btn.bind(on_press=self._on_add_item)
        row.add_widget(self._qty_input)
        row.add_widget(self._item_input)
        row.add_widget(add_btn)
        col1.add_widget(row)

        # Container to show pending items
        self._items_container = BoxLayout(orientation="vertical", size_hint=(1, 0.5))
        col1.add_widget(self._items_container)

        # Save button and status label
        save_row = BoxLayout(size_hint=(1, 0.1))
        save_btn = Button(text="Save Recipe", size_hint=(0.5, 1))
        save_btn.bind(on_press=self._on_save_recipe)
        self._status_label = Label(text="", size_hint=(0.5, 1))
        save_row.add_widget(save_btn)
        save_row.add_widget(self._status_label)
        col1.add_widget(save_row)

    def _on_add_item(self, instance):
        qty_text = (self._qty_input.text or "").strip()
        item_text = (self._item_input.text or "").strip()
        if not item_text or not qty_text.isdigit() or int(qty_text) <= 0:
            self._status_label.text = "Enter valid qty and item"
            return
        qty = int(qty_text)
        entry = f"{qty} {item_text}"
        self._pending_items.append(entry)
        # update UI list
        self._items_container.clear_widgets()
        app = App.get_running_app()
        for it in self._pending_items:
            self._items_container.add_widget(
                Label(
                    text=it, size_hint_y=None, height=dp(30) * (app.scale if app else 1)
                )
            )
        # clear inputs
        self._qty_input.text = ""
        self._item_input.text = ""
        self._status_label.text = f"{len(self._pending_items)} item(s) added"

    def _on_save_recipe(self, instance):
        title = (self._title_input.text or "").strip()
        if not title:
            self._status_label.text = "Enter recipe title"
            return
        if not self._pending_items:
            self._status_label.text = "Add at least one item"
            return
        ok = Recipes.add_recipe(title, self._pending_items)
        if ok:
            self._status_label.text = "Saved"
            # clear state and navigate back
            self._pending_items = []
            self._items_container.clear_widgets()
            self._title_input.text = ""
            # refresh the recipe list screen if present
            try:
                view_screen = self.sm.get_screen("ViewRecipesList")
                view_screen.initUI(self.sm)
            except Exception:
                pass
            self.sm.current = "RecipesMenu"
        else:
            self._status_label.text = "Save failed"

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            pass


class DeleteRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._title_input = None
        self._status_label = None

    def initUI(self, screen_manager_handle):
        # Setup with title and back button using helper
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Remove saved recipe",
            title_size="20",
            back_target="RecipesMenu",
        )

        self._title_input = TextInput(
            hint_text="Recipe title to delete", size_hint=(1, 0.1)
        )
        col1.add_widget(self._title_input)

        btn = Button(text="Delete", size_hint=(1, 0.1))
        btn.bind(on_press=self._on_delete)
        col1.add_widget(btn)

        self._status_label = Label(text="", size_hint=(1, 0.1))
        col1.add_widget(self._status_label)

    def _on_delete(self, instance):
        title = (self._title_input.text or "").strip()
        if not title:
            self._status_label.text = "Enter a title"
            return
        removed = Recipes.delete_recipe(title)
        if removed:
            self._status_label.text = "Deleted"
            # refresh list screen if present
            try:
                view_screen = self.sm.get_screen("ViewRecipesList")
                view_screen.initUI(self.sm)
            except Exception:
                pass
            self.sm.current = "RecipesMenu"
        else:
            self._status_label.text = "Not found"

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            pass


class RecipeDetailScreen(BaseScreen):
    """
    Shows the ingredient list for a selected recipe.
    Call `display_recipe(title)` before switching to this screen.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_scroll = None

    def initUI(self, screen_manager_handle):
        # Prepare layout and include Back to RecipesMenu
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Recipe Details",
            title_size="20",
            back_target="RecipesMenu",
        )

        btn = Button(text="Add to list", size_hint=(1, 0.1), on_press=self.button_click)
        col1.add_widget(btn)

        # no list populated at init; display_recipe will populate when a recipe is selected

    def display_recipe(self, title):
        """
        Update the title and populate the ingredient list for `title`.
        Removes any previous scroll/list widgets before adding new ones.
        """
        # ensure we have col1 / title
        if not hasattr(self, "col1") or self.col1 is None:
            return

        # set screen title
        if hasattr(self, "title") and self.title is not None:
            self.title.text = title

        # remove old lists if present
        to_remove = [w for w in list(self.col1.children) if isinstance(w, ScrollView)]
        for w in to_remove:
            self.col1.remove_widget(w)

        # get ingredients from Recipes implementation
        ingredients = Recipes.get_ingredients(title)
        if not ingredients:
            ingredients = ["(no ingredients found)"]

        # build a ScrollView with a GridLayout
        scroll = ScrollView(size_hint=(1, 1))
        list_grid = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        list_grid.bind(minimum_height=list_grid.setter("height"))

        app = App.get_running_app()
        for ingr in ingredients:
            lbl = Label(
                text=str(ingr),
                size_hint_y=None,
                height=dp(30) * (app.scale if app else 1),
            )
            list_grid.add_widget(lbl)

        scroll.add_widget(list_grid)
        self.col1.add_widget(scroll)
        self._current_scroll = scroll

    def button_click(self, instance):
        # Back button still uses BaseScreen.on_back
        if instance.text == "Back":
            self.on_back(instance)
        elif instance.text == "Add to list":
            # Instantiate ShoppingList and call the method that expects self
            sl = ShoppingList()
            sl.add_items_from_recipe_book(find_recipe=self.title.text)
            self.on_back(instance)
        else:
            pass


# Screen Template
# class SCREENNAME(BaseScreen):
#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#
#    def initUI(self, screen_manager_handle):
#        self.sm = screen_manager_handle
#        # Add Widgets to layout
#        self.master = BoxLayout()
#        col1 = BoxLayout(orientation='vertical',padding=15)
#
#        # Add Buttons and functionality here and then add to
#        # col1 with col1.addwidget()
#
#        # Add the menu to the row to appear on screen
#        self.master.add_widget(col1)
#
#        # now add this to myself
#        self.add_widget(self.master)
#
#
#    def button_click(self, instance):
#        option_text = instance.text
#
#        if option_text == "Back":
#            self.sm.current = "Home"
#        else:
#            pass
