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
from ShoppingList import ShoppingList
from BaseScreen import BaseScreen

Window.size = (500, 800)


class AddItemScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # Use helper to create a consistent title and back button
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Add item to list",
            title_size="45",
            back_target="Home",
        )

        # Fields and buttons specific to this screen
        self.num_items_input = TextInput(
            hint_text="Enter how many here", size_hint_y=0.2
        )
        self.item_name_input = TextInput(
            hint_text="Enter ingredient here", size_hint_y=0.2
        )
        self.add_btn = Button(
            text="Add",
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
            on_press=self.button_click,
        )

        # Add displays into col1
        col1.add_widget(self.num_items_input)
        col1.add_widget(self.item_name_input)
        col1.add_widget(self.add_btn)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        elif option_text == "Add":
            item = self.item_name_input.text.capitalize()
            num = self.num_items_input.text
            ShoppingList.add_item(f"{num} {item}")
            print(
                f"Add button pressed, num: {self.num_items_input.text} item: {self.item_name_input.text}"
            )
            self.sm.current = "Home"
        else:
            pass


class DeleteItemScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # Setup base layout with title and back button
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Remove item from list",
            title_size="20",
            back_target="Home",
        )

        self.item_name_input = TextInput(
            hint_text="Enter ingredient here", size_hint_y=0.2
        )

        # Buttons
        self.del_btn = Button(
            text="Delete",
            size_hint=(0.5, 0.2),
            pos_hint={"center_x": 0.5},
            on_press=self.button_click,
        )

        # Add specific widgets
        col1.add_widget(self.item_name_input)
        col1.add_widget(self.del_btn)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        elif option_text == "Delete":
            item = self.item_name_input.text
            ShoppingList.delete_item(item)
            print(f"delete button pressed. Deleting {item}")
            self.sm.current = "Home"
        else:
            pass


class ViewListScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="MyShoppingListApp",
            title_size="45",
            back_target="Home",
        )

        self.shopping_list = TextInput(
            font_size=45, size_hint_y=0.2, halign="left", multiline=True
        )

        # Add the shopping_text input to layout, then populate list below
        col1.add_widget(self.shopping_list)

        # read and add list items into the column
        self.read_items_from_file()

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        else:
            pass

    def read_items_from_file(self):
        self.list_of_items = ShoppingList.display()

        # Clear and re-add title/back to preserve them
        self.col1.clear_widgets()

        # Re-add base title and back button if they exist
        if hasattr(self, "title") and self.title:
            self.col1.add_widget(self.title)
        if hasattr(self, "back_btn") and self.back_btn:
            self.col1.add_widget(self.back_btn)

        # Reset the shopping_text input
        if hasattr(self, "shopping_list"):
            self.shopping_list.text = ""

        # populate list
        for i in self.list_of_items:
            if hasattr(self, "shopping_list"):
                self.shopping_list.text += i
            # add visible label rows
            list_item_handle = Label(
                text=f"{i}", size_hint=(1, 0.2), font_name="DejaVuSans"
            )
            self.col1.add_widget(list_item_handle)

    def on_enter(self, *args):
        """
        on_enter is a kivy hook, it runs when the button is clicked, so it is when the
        screen is entered this will run.  Because this class controls the list, we want
        to re-read from the file in case there were changes made to the list.
        """
        self.read_items_from_file()
        return


class AddIngredsFromRecipeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Add Ingredients to shopping list from recipe",
            title_size="20",
            back_target="Home",
        )

        # Text input for entering the recipe title
        self.recipe_title_input = TextInput(
            hint_text="Enter recipe title here", size_hint_y=0.2
        )

        # Button to trigger adding ingredients from the specified recipe
        self.add_from_recipe_btn = Button(
            text="Add From Recipe",
            size_hint=(0.6, 0.2),
            pos_hint={"center_x": 0.5},
            on_press=self.button_click,
        )

        # Add widgets to layout
        col1.add_widget(self.recipe_title_input)
        col1.add_widget(self.add_from_recipe_btn)

    def button_click(self, instance):
        option_text = instance.text

        if option_text == "Back":
            self.sm.current = "Home"
        elif option_text == "Add From Recipe":
            recipe_title = self.recipe_title_input.text.strip()
            if recipe_title:
                # Instantiate ShoppingList and call the method that expects self
                sl = ShoppingList()
                sl.add_items_from_recipe_book(find_recipe=recipe_title)
                print(f"Added ingredients from recipe: {recipe_title}")
            else:
                print("No recipe title entered; nothing added.")
            self.sm.current = "Home"
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
