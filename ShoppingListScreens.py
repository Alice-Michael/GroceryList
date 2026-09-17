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
from BaseScreen import BaseScreen

Window.size = (500, 800)


class AddItemScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="Add item to list", font_size='45', pos_hint={'top':1}, font_name="DejaVuSans")
        self.num_items_input = TextInput(hint_text = "Enter how many here", size_hint_y = 0.2)
        self.item_name_input = TextInput(hint_text = "Enter ingredient here", size_hint_y = 0.2)
        self.add_btn = Button(
            text = "Add",
            size_hint = (0.5, 0.2),
            pos_hint = {'center_x': 0.5},
            on_press = self.button_click
        )

        back_btn = self.get_back_button()

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)

        # Add displays into col1
        col1.add_widget(self.title)
        col1.add_widget(back_btn)
        col1.add_widget(self.num_items_input)
        col1.add_widget(self.item_name_input)
        col1.add_widget(self.add_btn)

        # Add the menu to the row to appear on screen
        self.master.add_widget(col1)

        # now add this to myself
        self.add_widget(self.master)


    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        elif option_text == "Add":
            item = self.item_name_input.text.capitalize()
            num = self.num_items_input.text
            ShoppingList.add_item_to_list_app(f"{num} {item}")
            print(f"Add button pressed, num: {self.num_items_input.text} item: {self.item_name_input.text}")
            self.sm.current = "Home"
        else:
            pass


class DeleteItemScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(
            text="Remove item from list",
            font_size='20',
            halign='left',
            valign='top',
            font_name="DejaVuSans"
        )
        self.item_name_input = TextInput(hint_text = "Enter ingredient here", size_hint_y = 0.2)

        #Buttons
        self.del_btn = Button(
            text = "Delete",
            size_hint = (0.5, 0.2),
            pos_hint = {'center_x': 0.5},
            on_press = self.button_click
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
            self.sm.current = "Home"
        elif option_text == "Delete":
            print(f"delete button pressed.  Deleting ")
        else:
            pass


class ViewListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="MyShoppingListApp", font_size='45', font_name="DejaVuSans")
        self.back_btn = self.get_back_button()

        self.shopping_list = TextInput(
            font_size = 45,
            size_hint_y = 0.2,
            halign = "left",
            multiline = True
        )

        # Add Widgets to layout
        self.master = BoxLayout()
        self.col1 = BoxLayout(orientation='vertical',padding=15)
        self.col1.add_widget(self.title)
        self.col1.add_widget(self.back_btn)

        self.read_items_from_file()

        # Add the menu to the row to appear on screen
        self.master.add_widget(self.col1)

        # now add this to myself
        self.add_widget(self.master)


    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        else:
            pass


    def read_items_from_file(self):
        self.list_of_items = ShoppingList.display_list_app()

        self.col1.clear_widgets()

        self.col1.add_widget(self.title)
        self.col1.add_widget(self.back_btn)

        for i in self.list_of_items:
            self.shopping_list.text += i
            list_item_handle = Label(
                text = f'{i}',
                size_hint = (1, 0.2),
                font_name = "DejaVuSans"
            )
            self.col1.add_widget(list_item_handle)


    def on_enter(self, *args):
        '''
        on_enter is a kivy hook, it runs when the button is clicked, so it is when the
        screen is entered this will run.  Because this class controls the list, we want
        to re-read from the file in case there were changes made to the list.
        '''
        self.read_items_from_file()

        return


class AddIngredsFromRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle

        self.title = Label(
            text="Add Ingredients to shopping list from recipe",
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
            self.sm.current = "Home"
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