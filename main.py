# kivy includes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.config import Config

import HomeScreen
import ShoppingListScreens
import RecipesScreens

Window.size = (500, 800)

class MainApp(App):
    # kivy looks for build
    def build(Self):
        # sm = Screen Manager
        sm = ScreenManager()
        homeScreenHandle = HomeScreen.Home(name="Home")
        view_shopping_list_handle = ShoppingListScreens.ViewListScreen(name="ViewList")
        add_item_handle = ShoppingListScreens.AddItemScreen(name="AddItem")
        delete_item_handle = ShoppingListScreens.DeleteItemScreen(name = "DelItemScreen")
        recipe_list_handle = RecipesScreens.RecipeViewList(name="ViewRecipesList")
        add_ingreds_from_recipe_handle = ShoppingListScreens.AddIngredsFromRecipeScreen(name = "addIngredsFromRecipe")
        recipes_menu_handle = RecipesScreens.RecipesMenu(name = "RecipesMenu")
        recipes_add_recipe_handle = RecipesScreens.AddRecipeScreen(name = "AddRecipeScreen")
        recipe_delete_handle = RecipesScreens.DeleteRecipeScreen(name = "DelRecipeScreen")

        homeScreenHandle.initUI(sm)
        view_shopping_list_handle.initUI(sm)
        add_item_handle.initUI(sm)
        delete_item_handle.initUI(sm)
        recipe_list_handle.initUI(sm)
        add_ingreds_from_recipe_handle.initUI(sm)
        recipes_menu_handle.initUI(sm)
        recipes_add_recipe_handle.initUI(sm)
        recipe_delete_handle.initUI(sm)

        sm.add_widget(homeScreenHandle)
        sm.add_widget(view_shopping_list_handle)
        sm.add_widget(add_item_handle)
        sm.add_widget(delete_item_handle)
        sm.add_widget(recipe_list_handle)
        sm.add_widget(add_ingreds_from_recipe_handle)
        sm.add_widget(recipes_menu_handle)
        sm.add_widget(recipes_add_recipe_handle)
        sm.add_widget(recipe_delete_handle)

        return sm


if __name__ == "__main__":
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')
    MainApp().run()