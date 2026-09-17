from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # default target for Back
        self.back_target = "Home"
        self.back_btn = None
        self.sm = None
        self.master = None
        self.col1 = None
        self.title = None

    def set_back_target(self, target):
        """Change where Back navigates to."""
        self.back_target = target

    def on_back(self, instance):
        """Default back handler can be overridden in subclasses."""
        if hasattr(self, "sm") and self.sm:
            self.sm.current = self.back_target

    def get_back_button(
        self, text="Back",
        size_hint=(1, 0.2),
        pos_hint={"center_x": 0.5}
    ):
        """
        Create (and store) a Back button wired to the default handler.
        Returns the Button so callers can add it to layouts.
        """
        self.back_btn = Button(
            text=text,
            size_hint=size_hint,
            pos_hint=pos_hint,
            on_press=self.on_back
        )
        return self.back_btn

    def setup_screen(
        self,
        screen_manager_handle,
        title_text: str = None,
        title_size: str = "20",
        font_name: str = "DejaVuSans",
        back_target: str = None,
        include_back: bool = True,
        padding: int = 15,
    ):
        """
        Common setup for screens:
        - sets self.sm
        - optionally sets back_target
        - creates self.master and self.col1 (vertical container)
        - optionally creates and adds a title label and back button
        - attaches master to the screen
        Returns (col1, back_btn) where back_btn may be None if include_back is False.
        """
        self.sm = screen_manager_handle
        if back_target:
            self.set_back_target(back_target)

        # create main layout containers
        self.master = BoxLayout()
        self.col1 = BoxLayout(orientation="vertical", padding=padding)

        # optional title
        self.back_btn = None
        if title_text:
            self.title = Label(
                text=title_text, font_size=title_size, font_name=font_name
            )
            self.col1.add_widget(self.title)

        # optional back button
        if include_back:
            self.back_btn = self.get_back_button()
            self.col1.add_widget(self.back_btn)

        # attach
        self.master.add_widget(self.col1)
        self.add_widget(self.master)

        return self.col1, self.back_btn

    def populate_list(
        self,
        col,
        items,
        font_name: str = "DejaVuSans",
        size_hint=(1, 0.2)
    ):
        """
        Add a sequence of string-like items as Labels into the provided column layout.
        """
        for i in items:
            list_item_handle = Label(
                text=str(i), size_hint=size_hint, font_name=font_name
            )
            col.add_widget(list_item_handle)
