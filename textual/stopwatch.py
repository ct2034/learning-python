from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header
from textual.color import Color

from random import random


class TimeDisplay(Digits):
    """A widget to display elapsed time."""

    def __init__(self, *args, **kwargs):
        super(TimeDisplay, self).__init__(*args, **kwargs)
        self.styles.background = Color(80 * random(), 80 * random(), 80 * random())


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")
        yield Button("-", id="minus", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "start":
            self.add_class("started")
        elif event.button.id == "stop":
            self.remove_class("started")
        elif event.button.id == "minus":
            self.remove()


class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "stopwatch.tcss"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("+", "plus", "Add stopwatch"),
    ]

    def __init__(self, *args, **kwargs):
        super(StopwatchApp, self).__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield VerticalScroll(Stopwatch(), id="timers")
        yield Button("+", id="plus", variant="primary")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_plus(self) -> None:
        """Add a stopwatch."""
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "plus":
            return
        self.action_plus()


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
