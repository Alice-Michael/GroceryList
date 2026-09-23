# kivy imports
from kivy.app import App
from kivy.metrics import sp, dp
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image


# Small Image-button class that preserves image aspect ratio and acts like a button
class IconButton(ButtonBehavior, Image):
    pass

# App imports
from ShoppingList import ShoppingList
from BaseScreen import BaseScreen


class AddItemScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initUI(self, screen_manager_handle):
        # Use helper to create a consistent title and back button
        col1, back_btn = self.setup_screen(
            screen_manager_handle,
            title_text="Add item to list",
            title_size="45",
            back_target="ViewListScreen",
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
            self.sm.current = "ViewListScreen"
        elif option_text == "Add":
            item = self.item_name_input.text.capitalize()
            num = self.num_items_input.text
            ShoppingList.add_item(f"{num} {item}")
            print(
                f"Add button pressed, num: {self.num_items_input.text} item: {self.item_name_input.text}"
            )
            # After adding, return to the view list screen
            self.sm.current = "ViewListScreen"
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

        # Add an Add-item button that navigates to the AddItemScreen
        add_btn = Button(text="Add item", size_hint=(1, 0.1))
        add_btn.bind(on_press=self._on_add_button)
        self.col1.add_widget(add_btn)

        # populate list as rows with a label and a delete button
        app = App.get_running_app()
        row_height = dp(40) * (app.scale if app else 1)
        for i in self.list_of_items:
            # horizontal row for item
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            row.spacing = dp(8) * (app.scale if app else 1)
            lbl = Label(text=f"{i}", size_hint_x=1, halign='left', valign='middle', font_name="DejaVuSans")
            lbl.bind(size=lbl.setter('text_size'))

            # delete button uses an image if available, otherwise fallback to text
            del_btn = IconButton(
                source='x_icon.png',
                size_hint_x=None,
                width=row_height * 0.8,
                allow_stretch=False,
                keep_ratio=True,
            )
            try:
                # try to use an x icon file named 'x_icon.png'
                del_btn.background_normal = 'x_icon.png'
                del_btn.background_down = 'x_icon.png'
                del_btn.text = ''
                # ensure button uses the image as-is
                del_btn.background_color = (1, 1, 1, 1)
            except Exception:
                del_btn.text = 'Del'

            # bind delete action; capture current item in default arg
            def _on_del(instance, item=i):
                ShoppingList.delete_item(item)
                # refresh list view after delete
                self.read_items_from_file()

            del_btn.bind(on_press=_on_del)

            # place delete button on the left, label to the right
            row.add_widget(del_btn)
            row.add_widget(lbl)
            self.col1.add_widget(row)

    def on_enter(self, *args):
        """
        on_enter is a kivy hook, it runs when the button is clicked, so it is when the
        screen is entered this will run.  Because this class controls the list, we want
        to re-read from the file in case there were changes made to the list.
        """
        self.read_items_from_file()
        return

    def _on_add_button(self, instance):
        # Navigate to the add-item screen
        if hasattr(self, 'sm') and self.sm:
            self.sm.current = 'AddItemScreen'


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
