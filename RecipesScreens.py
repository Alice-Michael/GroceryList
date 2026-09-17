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
import Recipes
from BaseScreen import BaseScreen

Window.size = (500, 800)

recipes_menu_options = [
    "Show Recipes",
    "Add recipe",
    "Delete recipe",
    "Back"
]

class RecipesMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle

        self.title = Label(text="Recipes Menu", font_size='20', font_name="DejaVuSans")

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)
        
        # Add Buttons and functionality here and then add to 
        # col1 with col1.addwidget()
        col1.add_widget(self.title)
        for i in recipes_menu_options:
            btn = Button(
                text= f'{i}',
                size_hint=(1, 0.2), 
                pos_hint={'center_x':0.5},
                on_press = self.button_click
            )
            col1.add_widget(btn)
        
        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


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
        self.sm = screen_manager_handle
        # make Back go to RecipesMenu instead of default Home
        self.set_back_target("RecipesMenu")

        self.title = Label(text="Shopping List", font_size='20', font_name="DejaVuSans")
        self.back_btn = self.get_back_button()

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)
        
        # Add Buttons and functionality here and then add to 
        # col1 with col1.addwidget()
        col1.add_widget(self.title)
        col1.add_widget(self.back_btn)

        list_of_recipes = Recipes.display_list_app()
        for i in list_of_recipes:
            list_item_handle = Label(
                text = f'{i}',
                size_hint = (1, 0.2),
                font_name = "DejaVuSans"
            )
            col1.add_widget(list_item_handle)

        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            pass


class AddRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.set_back_target("RecipesMenu")
        self.title = Label(text="Add saved recipe", font_size='20', pos_hint={'top':1}, font_name="DejaVuSans")
        back_btn = self.get_back_button()

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)

        # Add displays into col1
        col1.add_widget(self.title)
        col1.add_widget(back_btn)

        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


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
        self.sm = screen_manager_handle
        self.set_back_target("RecipesMenu")
        self.title = Label(
            text="Remove saved recipe",
            font_size='20',
            halign='left',
            valign='top',
            font_name="DejaVuSans"
        )
        self.back_btn = self.get_back_button()

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)

        # Add Buttons and functionality here and then add to
        # col1 with col1.addwidget()
        col1.add_widget(self.title)
        col1.add_widget(self.back_btn)

        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "RecipesMenu"
        else:
            pass


# Screen Template
#class SCREENNAME(BaseScreen):
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