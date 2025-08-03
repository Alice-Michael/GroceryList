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


class AddItemScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="Add item to list", font_size='45', pos_hint={'top':1}, font_name="DejaVuSans")
        back_btn = Button(
            text="Back",
            size_hint=(1, 0.2), 
            pos_hint={'center_x':0.5},
            on_press = self.button_click
        )

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
            self.sm.current = "Home"
        else:
            pass

class ViewListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        self.sm = screen_manager_handle
        self.title = Label(text="MyShoppingListApp", font_size='45', font_name="DejaVuSans")
        self.back_btn = Button(
            text="Back",
            size_hint=(1, 0.2), 
            pos_hint={'center_x':0.5},
            on_press = self.button_click
        )

        self.shopping_list = TextInput(
            font_size = 45,
            size_hint_y = 0.2,
            halign = "left",
            multiline = True
        )

        # Add Widgets to layout
        self.master = BoxLayout()
        col1 = BoxLayout(orientation='vertical',padding=15)
        col1.add_widget(self.title)
        col1.add_widget(self.back_btn)

        list_of_items = ShoppingList.display_list_app()
        for i in list_of_items:
            self.shopping_list.text += i
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
            self.sm.current = "Home"
        else:
            pass


class AddIngredsFromRecipeScreen(Screen):
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
        self.back_btn = Button(
            text="Back",
            size_hint=(1, 0.2),
            pos_hint={'center_x':0.5},
            on_press = self.button_click
        )

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


class DeleteItemScreen(Screen):
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
        self.back_btn = back_btn = Button(
            text="Back",
            size_hint=(1, 0.2),
            pos_hint={'center_x':0.5},
            on_press = self.button_click
        )

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
#class SCREENNAME(Screen):
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