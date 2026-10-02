import os
import sys

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class ErrorScreen(Screen):
    def __init__(self, **kwargs):
        super(ErrorScreen, self).__init__(name="error_screen", **kwargs)

        # Main vertical layout with spacing and padding
        layout = BoxLayout(orientation="vertical", spacing=20, padding=40)

        heading = Label(
            text="Something Went Wrong",
            font_size="24sp",
            bold=True,
            size_hint_y=None,
            height=40,
        )

        # User Instructions
        log_path = os.path.abspath("crash_log.txt")
        instructions_text = (
            "An error occurred during application setup.\n\n"
            "To help fix this, please log a report with the developer.\n"
            f"If possible, include the log file located at:\n[b]{log_path}[/b]"
        )

        instructions = Label(
            text=instructions_text,
            font_size="16sp",
            halign="center",
            valign="middle",
            markup=True,  # Enables the bold formatting for the file path
        )
        instructions.bind(size=instructions.setter("text_size"))

        # Action Button to exit cleanly
        exit_btn = Button(
            text="Close Application",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={"center_x": 0.5},
        )
        exit_btn.bind(on_release=self.close_app)

        # Assemble the UI
        layout.add_widget(heading)
        layout.add_widget(instructions)
        layout.add_widget(exit_btn)
        self.add_widget(layout)

    def close_app(self, instance):
        App.get_running_app().stop()
        sys.exit(0)
