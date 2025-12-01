from textual.app import ComposeResult
from textual.widgets import Input, Label, Button
from textual.containers import Container, Vertical
from textual.screen import ModalScreen

class AddFeedScreen(ModalScreen[str]):
    # simple modal to ask for a url
    CSS = """
    AddFeedScreen {
        align: center middle;
    }
    #dialog {
        padding: 0 1;
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }
    Label { margin: 1 0; }
    Input { margin-bottom: 1; }
    #buttons {
        layout: horizontal;
        align: right middle;
        height: auto;
    }
    Button { margin-left: 1; }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Enter RSS Feed URL:")
            yield Input(placeholder="https://...", id="url_input")
            with Container(id="buttons"):
                yield Button("Cancel", variant="error", id="cancel")
                yield Button("Add", variant="primary", id="add")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            input_widget = self.query_one("#url_input", Input)
            if input_widget.value:
                # pass the value back to the main app
                self.dismiss(input_widget.value)
        else:
            self.dismiss(None)