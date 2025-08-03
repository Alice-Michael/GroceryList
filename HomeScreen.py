# python
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
import ShoppingList

Window.size = (500, 800)

menu_options = [
    "View List",
    "Add Item",
    "Delete Item",
    "Add ingredients from recipe",
    "Recipes menu"
]

recipes_menu_options = [
    "Show Recipes",
    "Add recipe",
    "Delete recipe"
]

class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="MyShoppingListApp", font_size='45', font_name="DejaVuSans")

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)

        # Make the first item the banner title.
        col1.add_widget(self.title)

        # Menu options
        for i in menu_options:
            btn = Button(
                text = f'{i}',
                size_hint = (1, 0.2),
                pos_hint = {'center_x':0.5},
                on_press = self.button_click
            )
            col1.add_widget(btn)

        self.shopping_list = TextInput(
            font_size = 45,
            size_hint_y = 0.2,
            halign = "left",
            multiline = True
        )

        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


    def button_click(self, instance):
        text = instance.text

        if text == "View List":
            self.sm.current = "ViewList"
        elif text == "Add Item":
            self.sm.current = "AddItem"
        elif text == "Delete Item":
            pass
        elif text == "Add ingredients from recipe":
            pass
        elif text == "Recipes menu":
            self.sm.current = "RecipesMenu"
        else:
            pass