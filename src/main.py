# main.py

"""
Main entry point for the Lore Games application.

This script now launches the Textual-based user interface.
"""

from .tui import LoreGamesApp

def main():
    """Initializes and runs the TUI application."""
    app = LoreGamesApp()
    app.run()

if __name__ == "__main__":
    main()