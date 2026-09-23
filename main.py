# kivy includes
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.utils import platform

class MyScreenManager(ScreenManager):
    pass

class MyApp(App):
    scale = NumericProperty(1.0)
    BASE_WIDTH = 360.0
    BASE_HEIGHT = 640.0

    def build(self):
        # Load Home screen implementation from HomeScreen.py and initialize it
        try:
            from HomeScreen import Home
        except Exception:
            Home = None
        if platform == 'android':
            Window.fullscreen = 'auto'
        self._update_scale(Window.size)
        Window.bind(on_resize=self._on_window_resize)
        # Create ScreenManager and register screens from other modules
        sm = MyScreenManager()

        # Home screen
        if Home:
            h = Home(name='Home')
            try:
                h.initUI(sm)
            except Exception as e:
                # Log traceback so initialization errors are visible during startup
                import traceback
                print("Error initializing Home screen:")
                traceback.print_exc()
            sm.add_widget(h)

        # Import and register shopping list screens
        try:
            from ShoppingListScreens import (
                AddItemScreen,
                DeleteItemScreen,
                ViewListScreen,
                AddIngredsFromRecipeScreen,
            )

            s = AddItemScreen(name='AddItemScreen')
            try:
                s.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing AddItemScreen:")
                traceback.print_exc()
            sm.add_widget(s)

            s = DeleteItemScreen(name='DeleteItemScreen')
            try:
                s.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing DeleteItemScreen:")
                traceback.print_exc()
            sm.add_widget(s)

            s = ViewListScreen(name='ViewListScreen')
            try:
                s.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing ViewListScreen:")
                traceback.print_exc()
            sm.add_widget(s)

            s = AddIngredsFromRecipeScreen(name='AddIngredsFromRecipeScreen')
            try:
                s.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing AddIngredsFromRecipeScreen:")
                traceback.print_exc()
            sm.add_widget(s)
        except Exception:
            import traceback
            print("Error importing ShoppingListScreens:")
            traceback.print_exc()

        # Import and register recipe screens
        try:
            from RecipesScreens import (
                RecipesMenu,
                RecipeViewList,
                AddRecipeScreen,
                DeleteRecipeScreen,
                RecipeDetailScreen,
            )

            r = RecipesMenu(name='RecipesMenu')
            try:
                r.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing RecipesMenu:")
                traceback.print_exc()
            sm.add_widget(r)

            r = RecipeViewList(name='ViewRecipesList')
            try:
                r.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing RecipeViewList:")
                traceback.print_exc()
            sm.add_widget(r)

            r = AddRecipeScreen(name='AddRecipeScreen')
            try:
                r.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing AddRecipeScreen:")
                traceback.print_exc()
            sm.add_widget(r)

            r = DeleteRecipeScreen(name='DelRecipeScreen')
            try:
                r.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing DeleteRecipeScreen:")
                traceback.print_exc()
            sm.add_widget(r)

            r = RecipeDetailScreen(name='RecipeDetail')
            try:
                r.initUI(sm)
            except Exception:
                import traceback
                print("Error initializing RecipeDetail:")
                traceback.print_exc()
            sm.add_widget(r)
        except Exception:
            import traceback
            print("Error importing RecipesScreens:")
            traceback.print_exc()

        return sm

    def _on_window_resize(self, window, width, height):
        self._update_scale((width, height))

    def _update_scale(self, size):
        width, height = size
        scale_w = width / self.BASE_WIDTH
        scale_h = height / self.BASE_HEIGHT
        self.scale = min(scale_w, scale_h)

if __name__ == '__main__':
    MyApp().run()