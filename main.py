# kivy includes
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.utils import platform

# Home UI is implemented in HomeScreen.py (class `Home`) to keep layouts out of inline KV

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

        # Home screen (initialize via Home.initUI so layout/back button work)
        if Home:
            h = Home(name='Home')
            try:
                h.initUI(sm)
            except Exception:
                # fallback: add the screen without explicit init
                pass
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
            s.initUI(sm)
            sm.add_widget(s)

            s = DeleteItemScreen(name='DeleteItemScreen')
            s.initUI(sm)
            sm.add_widget(s)

            s = ViewListScreen(name='ViewListScreen')
            s.initUI(sm)
            sm.add_widget(s)

            s = AddIngredsFromRecipeScreen(name='AddIngredsFromRecipeScreen')
            s.initUI(sm)
            sm.add_widget(s)
        except Exception:
            # If the module isn't present or fails to initialize, skip registering
            pass

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
            r.initUI(sm)
            sm.add_widget(r)

            r = RecipeViewList(name='ViewRecipesList')
            r.initUI(sm)
            sm.add_widget(r)

            r = AddRecipeScreen(name='AddRecipeScreen')
            r.initUI(sm)
            sm.add_widget(r)

            r = DeleteRecipeScreen(name='DelRecipeScreen')
            r.initUI(sm)
            sm.add_widget(r)

            r = RecipeDetailScreen(name='RecipeDetail')
            r.initUI(sm)
            sm.add_widget(r)
        except Exception:
            pass

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