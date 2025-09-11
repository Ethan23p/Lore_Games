from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Button, Input, ListView, ListItem, Label, RichLog
from textual import on
from textual.theme import Theme

# Configurable 5-color scheme
# Darkest brown (#1F1E1D)
# Dark brown (#262624)
# Light cream (#BFBDB8)
# Coral orange (#D97059)
# Golden cream (#BFAF80)
COLORS = {
    "primary": "#262624",      # Dark brown (main background)
    "secondary": "#1F1E1D",    # Darkest brown (accent areas)
    "text": "#BFBDB8",         # Light cream (text color)
    "accent": "#D97059",       # Coral orange (highlights, buttons)
    "border": "#BFAF80",       # Golden cream (borders)
    "emphasis": "#BFAF80",     # Golden cream (emphasis text)
}

# Create a custom theme with our colors
CUSTOM_THEME = Theme(
    "creamy-dark",  # theme name
    COLORS["primary"],  # primary color
    secondary=COLORS["secondary"], 
    foreground=COLORS["text"],
    accent=COLORS["accent"],
    surface=COLORS["secondary"],
    background=COLORS["primary"],
    panel=COLORS["secondary"],
    error=COLORS["accent"],
    warning=COLORS["accent"],
    success=COLORS["border"],
    variables={
        "border": COLORS["primary"],
        "emphasis": COLORS["emphasis"],
    }
)

# A list of mock threads for the sidebar
THREADS = ["General", "Python", "Textual", "Chat", "Help"]

# Mock conversation data for each thread
CONVERSATIONS = {
    thread: [
        f"[bold {COLORS['accent']}]AI:[/bold {COLORS['accent']}] Welcome to the '{thread}' thread.",
        f"[bold {COLORS['emphasis']}]User:[/bold {COLORS['emphasis']}] Tell me something about this topic.",
        f"[bold {COLORS['accent']}]AI:[/bold {COLORS['accent']}] This is a mock conversation about '{thread}'. The possibilities are endless!",
    ]
    for thread in THREADS
}

# Add some additional messages to the first thread
CONVERSATIONS["General"].extend([
    f"[bold {COLORS['emphasis']}]User:[/bold {COLORS['emphasis']}] Can you elaborate?",
    f"[bold {COLORS['accent']}]AI:[/bold {COLORS['accent']}] Certainly. This demonstrates how selecting a thread can dynamically update the main content area with relevant history.",
])


class ChatApp(App):
    """A simple chat TUI application built with Textual."""

    CSS_PATH = "chat.tcss"
    TITLE = "Agent Dashboard"
    SUB_TITLE = "Interface for interacting with sophisticated AI agents."

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # The main layout consists of a sidebar, a main content area, and an input bar.
        # Docking is used to fix the sidebar and input bar to the edges.
        yield Header()
        with Container(id="app-grid"):
            yield ListView(
                *[ListItem(Label(thread)) for thread in THREADS], id="thread-list"
            )
            with Container(id="main-content"):
                yield RichLog(id="chat-history", wrap=True, highlight=False, markup=True)
                with Horizontal(id="input-bar"):
                    yield Input(placeholder="How can I help you today?", id="message-input")
                    yield Button("↑", id="send-button", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        # Register and apply our custom theme
        self.register_theme(CUSTOM_THEME)
        self.theme = "creamy-dark"
        
        # Focus the input field and load the first conversation by default.
        self.query_one("#message-input").focus()
        self.query_one(ListView).index = 0
        self.load_conversation(THREADS[0])

    def load_conversation(self, thread_name: str) -> None:
        """Clears the chat log and loads messages for the selected thread."""
        chat_log = self.query_one(RichLog)
        chat_log.clear()
        for message in CONVERSATIONS.get(thread_name, []):
            chat_log.write(message)

    @on(ListView.Selected)
    def on_thread_selected(self, event: ListView.Selected) -> None:
        """Handle the selection of a new thread in the sidebar."""
        thread_name = event.item.query_one(Label).renderable
        self.load_conversation(str(thread_name))

    def action_send_message(self) -> None:
        """Called when the user sends a message."""
        message_input = self.query_one("#message-input", Input)
        chat_log = self.query_one("#chat-history", RichLog)

        message_text = message_input.value
        if message_text:
            # Add the user's message to the log and clear the input.
            chat_log.write(f"[bold {COLORS['emphasis']}]User:[/bold {COLORS['emphasis']}] {message_text}")
            message_input.value = ""
            # A mock AI response for demonstration purposes.
            chat_log.write(f"[bold {COLORS['accent']}]AI:[/bold {COLORS['accent']}] That's an interesting thought.")
            chat_log.scroll_end(animate=True)

    @on(Button.Pressed, "#send-button")
    def on_button_pressed(self) -> None:
        """Handle send button clicks."""
        self.action_send_message()

    @on(Input.Submitted, "#message-input")
    def on_input_submitted(self) -> None:
        """Handle 'Enter' key press in the input field."""
        self.action_send_message()


if __name__ == "__main__":
    app = ChatApp()
    app.run()