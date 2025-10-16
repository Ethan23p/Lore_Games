# tui.py

import os
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Button, Markdown, ListView, ListItem, Label, Input
from textual import on, work
from textual.theme import Theme

from .app import SimulationEngine

# Color scheme from the reference app
COLORS = {
    "primary": "#262624",
    "secondary": "#1F1E1D",
    "text": "#BFBDB8",
    "accent": "#D97059",
    "border": "#BFAF80",
    "emphasis": "#BFAF80",
}

CUSTOM_THEME = Theme(
    "creamy-dark",
    COLORS["primary"],
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

class LoreGamesApp(App):
    """A Textual interface for the Lore Games simulation."""

    CSS_PATH = "tui.tcss"
    TITLE = "Lore Games"

    def __init__(self):
        super().__init__()
        self.simulation = SimulationEngine()
        self.current_view = "Environment" # Default view

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        with Header():
            yield Label("", id="loading-status")
        with Container(id="app-grid"):
            yield ListView(
                ListItem(Label("Environment"), id="Environment"),
                ListItem(Label("Charlie"), id="Charlie"),
                ListItem(Label("Delta"), id="Delta")
            , id="navigator")
            with Container(id="main-content"):
                yield Markdown(id="main-log")
                with Horizontal(id="input-container"):
                    yield Input(placeholder="Future commands...", disabled=True, id="main-input")
        yield Button("Next Turn", id="next-turn-button", variant="primary")
        yield Footer()

    async def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.register_theme(CUSTOM_THEME)
        self.theme = "creamy-dark"
        markdown_viewer = self.query_one(Markdown)
        markdown_viewer.update("## Initializing Simulation...")
        await self.simulation.initialize_simulation()
        markdown_viewer.update("## Simulation Initialized. Ready for Turn 1.")
        self.query_one("#next-turn-button").focus()
        await self._update_main_log()

    async def _update_main_log(self):
        """Reads the appropriate log file and updates the main content view."""
        markdown_viewer = self.query_one(Markdown)
        turn_dir = os.path.join("state_dump", f"turn_{self.simulation.current_turn:03d}")

        file_map = {}
        if self.simulation.current_turn == 0:
            file_map = {
                "Environment": None,  # Special case for initial reality
                "Charlie": "Charlie_initial_perspective.md",
                "Delta": "Delta_initial_perspective.md",
            }
        elif self.simulation.current_turn == 1:
            file_map = {
                "Environment": "environment_divination.md",
                "Charlie": "Charlie_perspective.md",
                "Delta": "Delta_perspective.md",
            }
        else:
            file_map = {
                "Environment": "environment_divination.md",
                "Charlie": "Charlie_intention.md",
                "Delta": "Delta_intention.md",
            }

        if self.current_view == "Environment" and self.simulation.current_turn == 0:
            content = f"""## Displaying: Initial Reality (Turn 0)\n\n{self.simulation.environment.reality[0].content if self.simulation.environment else ''}"""
            markdown_viewer.update(content)
            return

        filename = file_map.get(self.current_view)
        if not filename:
            markdown_viewer.update(f"## No view available for '{self.current_view}' in Turn {self.simulation.current_turn}")
            return

        filepath = os.path.join(turn_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            markdown_viewer.update(content)
        except FileNotFoundError:
            markdown_viewer.update(f"## Log file not found for {self.current_view} in Turn {self.simulation.current_turn}\nPath: {filepath}")

    @on(ListView.Selected)
    async def on_view_selected(self, event: ListView.Selected) -> None:
        """Handle the selection of a new view in the sidebar."""
        if event.item.id:
            self.current_view = event.item.id
            await self._update_main_log()

    @on(Button.Pressed, "#next-turn-button")
    def on_next_turn_button(self) -> None:
        """Handle the 'Next Turn' button press by starting the worker."""
        self.query_one("#next-turn-button").disabled = True
        self.run_turn_worker()

    @work(thread=True)
    async def run_turn_worker(self) -> None:
        """Runs a single simulation turn in a background thread."""
        status_label = self.query_one("#loading-status", Label)
        try:
            self.call_from_thread(status_label.update, "🔄 Generating...")
            await self.simulation.run_single_turn()
            await self._update_main_log()
        except Exception as e:
            # If there's an error, we can show it in the log
            log_view = self.query_one(Markdown)
            self.call_from_thread(log_view.update, f"[bold red]An error occurred during the simulation: {e}[/bold red]")
        finally:
            # Clear status and re-enable button
            self.call_from_thread(status_label.update, "")
            self.call_from_thread(setattr, self.query_one("#next-turn-button"), "disabled", False)

if __name__ == "__main__":
    app = LoreGamesApp()
    app.run()
