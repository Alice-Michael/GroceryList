# python
# kivy imports (trimmed: keep only used symbols)
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

Window.size = (500, 800)

menu_options = [
    "View list",
    "Add item",
    "Delete item",
    "Add ingredients from recipe",
    "Recipes menu",
]


class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="Get Food", font_size='45', font_name="DejaVuSans")

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical', padding=15)

        # Logo (if present) above the title
        try:
            logo = Image(source='logo.jpg', size_hint=(1, 1))
            col1.add_widget(logo)
        except Exception:
            # If image fails to load, continue without breaking the UI
            pass

        # Make the first visible item the banner title.
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

        # Map menu labels to the screen names registered in main.py
        if text == "View list":
            self.sm.current = "ViewListScreen"
        elif text == "Add item":
            self.sm.current = "AddItemScreen"
        elif text == "Delete item":
            self.sm.current = "DeleteItemScreen"
        elif text == "Add ingredients from recipe":
            self.sm.current = "AddIngredsFromRecipeScreen"
        elif text == "Recipes menu":
            self.sm.current = "RecipesMenu"
        else:
            pass
