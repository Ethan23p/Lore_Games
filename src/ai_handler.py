# src/ai_handler.py

# Use TYPE_CHECKING to avoid circular import at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.lore_types import Agent, Environment

class AIHandler:
    """
    A generic handler for passing a prompt string to an AI and returning
    its response.
    """
    def __init__(self):
        pass

    def generate(self, prompt: str) -> str:
        """
        Generates an AI response.
        """
        # --- Generate AI response (mocked) ---
        mock_response = f"Mock AI response to:\n---\n{prompt}\n---"
        return mock_response
