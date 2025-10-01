# main.py

import asyncio
from app import LoreGamesApp

async def main():
    """The main entry point for the application."""
    game_app = LoreGamesApp()
    await game_app.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSimulation exited.")