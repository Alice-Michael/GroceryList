# kivy imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

# App imports
from Recipes import Recipes
from BaseScreen import BaseScreen

Window.size = (500, 800)

recipes_menu_options = ["Show Recipes", "Add recipe", "Delete recipe", "Back"]


class RecipesMenu(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        # populate items using helper
        self.populate_list(col1, list_of_recipes)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            # item presses can be handled here
            pass


class AddRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # setup base layout with back target
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Add saved recipe",
            title_size="20",
            back_target="RecipesMenu",
        )

        # Add additional widgets if necessary; kept minimal per original

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            pass


class DeleteRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # Setup with title and back button using helper
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Remove saved recipe",
            title_size="20",
            back_target="RecipesMenu",
        )

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
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
