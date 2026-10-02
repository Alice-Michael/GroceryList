# kivy includes
import traceback

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import mainthread
from kivy.metrics import dp

# App
from GUI.HomeScreen import Home
from GUI.ShoppingListScreens import (
    AddItemScreen,
    ViewListScreen,
    AddIngredsFromRecipeScreen,
)
from GUI.RecipesScreens import (
    RecipesMenu,
    RecipeViewList,
    AddRecipeScreen,
    DeleteRecipeScreen,
    RecipeDetailScreen,
)


class MyRootLayout(BoxLayout):
    """
    Root layout that contains a content area (where the ScreenManager is placed)
    and a bottom spacer widget whose height can be adjusted to account for
    Android system UI (navigation bar) insets.
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        # main content area where we'll add the ScreenManager
        self.content_area = BoxLayout(orientation="vertical")
        self.add_widget(self.content_area)

        # bottom spacer initially zero height
        self.bottom_spacer = Widget(size_hint_y=None, height=0)
        self.add_widget(self.bottom_spacer)


class MyApp(App):
    scale = NumericProperty(1.0)
    BASE_WIDTH = 360.0
    BASE_HEIGHT = 640.0

    def build(self):
        # Build a root layout that reserves a bottom spacer for system UI insets
        root = MyRootLayout()

        if platform == "android":
            Window.fullscreen = "auto"

        # Create ScreenManager and register screens from other modules
        sm = ScreenManager()

        # Home screen
        if Home:
            h = Home(name="Home")
            try:
                h.initUI(sm)
            except Exception:
                print("Error initializing Home screen:")
                traceback.print_exc()
            sm.add_widget(h)

        # Register shopping list screens
        s = AddItemScreen(name="AddItemScreen")
        try:
            s.initUI(sm)
        except Exception:
            print("Error initializing AddItemScreen:")
            traceback.print_exc()
        sm.add_widget(s)

        s = ViewListScreen(name="ViewListScreen")
        try:
            s.initUI(sm)
        except Exception:
            print("Error initializing ViewListScreen:")
            traceback.print_exc()
        sm.add_widget(s)

        s = AddIngredsFromRecipeScreen(name="AddIngredsFromRecipeScreen")
        try:
            s.initUI(sm)
        except Exception:
            print("Error initializing AddIngredsFromRecipeScreen:")
            traceback.print_exc()
        sm.add_widget(s)

        # Register recipe screens
        r = RecipesMenu(name="RecipesMenu")
        try:
            r.initUI(sm)
        except Exception:
            print("Error initializing RecipesMenu:")
            traceback.print_exc()
        sm.add_widget(r)

        r = RecipeViewList(name="ViewRecipesList")
        try:
            r.initUI(sm)
        except Exception:
            print("Error initializing RecipeViewList:")
            traceback.print_exc()
        sm.add_widget(r)

        r = AddRecipeScreen(name="AddRecipeScreen")
        try:
            r.initUI(sm)
        except Exception:
            print("Error initializing AddRecipeScreen:")
            traceback.print_exc()
        sm.add_widget(r)

        r = DeleteRecipeScreen(name="DelRecipeScreen")
        try:
            r.initUI(sm)
        except Exception:
            print("Error initializing DeleteRecipeScreen:")
            traceback.print_exc()
        sm.add_widget(r)

        r = RecipeDetailScreen(name="RecipeDetail")
        try:
            r.initUI(sm)
        except Exception:
            print("Error initializing RecipeDetail:")
            traceback.print_exc()
        sm.add_widget(r)

        # Put the ScreenManager into the root layout's content area
        root.content_area.add_widget(sm)

        # Keep references for inset adjustments
        self.root_layout = root

        # Update scaling and bind resize
        self._update_scale(Window.size)
        Window.bind(on_resize=self._on_window_resize)

        return root

    def _on_window_resize(self, window, width, height):
        self._update_scale((width, height))
        # Re-apply Android insets (if running on device)
        try:
            if hasattr(self, "apply_android_insets"):
                self.apply_android_insets()
        except Exception:
            pass

    def on_start(self):
        # Apply Android insets once the app is running
        if platform == "android":
            try:
                self.apply_android_insets()
            except Exception:
                pass

    @mainthread
    def apply_android_insets(self):
        # Adjust the bottom spacer in the root layout using WindowInsets if available
        if not hasattr(self, "root_layout"):
            return
        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity
            window = activity.getWindow()
            decor_view = window.getDecorView()

            # Attempt to read modern WindowInsets
            insets = None
            try:
                insets = decor_view.getRootWindowInsets()
            except Exception:
                insets = None

            bottom_px = 0
            if insets is not None:
                try:
                    Type = autoclass("android.view.WindowInsets$Type")
                    system_bars = insets.getInsets(Type.systemBars())
                    bottom_px = int(system_bars.bottom)
                except Exception:
                    try:
                        bottom_px = int(insets.getStableInsetBottom())
                    except Exception:
                        bottom_px = 0

            # Fallback: compute difference between real and usable metrics
            if bottom_px == 0:
                try:
                    DisplayMetrics = autoclass("android.util.DisplayMetrics")
                    display = activity.getWindowManager().getDefaultDisplay()
                    real = DisplayMetrics()
                    usable = DisplayMetrics()
                    try:
                        display.getRealMetrics(real)
                        display.getMetrics(usable)
                        bottom_px = max(0, real.heightPixels - usable.heightPixels)
                    except Exception:
                        # Resource lookup fallback
                        resources = activity.getResources()
                        res_id = resources.getIdentifier(
                            "navigation_bar_height", "dimen", "android"
                        )
                        if res_id:
                            bottom_px = resources.getDimensionPixelSize(res_id)
                except Exception:
                    bottom_px = 0

            # Convert Android px to Kivy units
            if bottom_px and hasattr(Window, "height") and decor_view.getHeight():
                kivy_gap = bottom_px * (
                    float(Window.height) / float(decor_view.getHeight())
                )
            elif bottom_px:
                kivy_gap = bottom_px
            else:
                kivy_gap = dp(80)

            # Set the spacer height
            try:
                self.root_layout.bottom_spacer.height = kivy_gap
            except Exception:
                pass
        except Exception:
            # If anything fails, use a conservative dp-based spacer
            try:
                self.root_layout.bottom_spacer.height = dp(80)
            except Exception:
                pass

    def _update_scale(self, size):
        width, height = size
        scale_w = width / self.BASE_WIDTH
        scale_h = height / self.BASE_HEIGHT
        self.scale = min(scale_w, scale_h)


if __name__ == "__main__":
    MyApp().run()
