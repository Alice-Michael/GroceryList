# python
# kivy imports (trimmed: keep only used symbols)
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.metrics import sp, dp

menu_options = [
    "View list",
    "Add ingredients from recipe",
    "Recipes menu",
]


class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        app = App.get_running_app()
        self.title = Label(text="Get Food", font_size=sp(24) * (app.scale if app else 1), font_name="DejaVuSans")

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical', padding=15)

        # Logo (if present) above the title
        try:
            # Limit logo to the top portion so menu remains visible
            logo = Image(source='logo.png', size_hint=(1, 1))
            print(f"Home: logo widget created, source=logo.jpg")
            col1.add_widget(logo)
        except Exception as e:
            # If image fails to load, continue without breaking the UI
            print(f"Home: failed to load logo: {e}")

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
            font_size=sp(16) * (app.scale if app else 1),
            size_hint_y=0.2,
            halign="left",
            multiline=True,
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
        elif text == "Add ingredients from recipe":
            self.sm.current = "AddIngredsFromRecipeScreen"
        elif text == "Recipes menu":
            self.sm.current = "RecipesMenu"
        else:
            pass
