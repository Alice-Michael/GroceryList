from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # default target for Back
        self.back_target = "Home"
        self.back_btn = None
        self.sm = None

    def set_back_target(self, target):
        """Change where Back navigates to."""
        self.back_target = target

    def on_back(self, instance):
        """Default back handler can be overridden in subclasses."""
        if hasattr(self, "sm") and self.sm:
            self.sm.current = self.back_target

    def get_back_button(self, text="Back", size_hint=(1, 0.2), pos_hint={'center_x':0.5}):
        """
        Create (and store) a Back button wired to the default handler.
        Returns the Button so callers can add it to layouts.
        """
        self.back_btn = Button(text=text, size_hint=size_hint, pos_hint=pos_hint, on_press=self.on_back)
        return self.back_btn
