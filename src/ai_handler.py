# ai_handler.py

import asyncio
from google import genai
from google.genai import types
from google.api_core.exceptions import GoogleAPICallError

# Define a custom exception for our application.
class AIGenerationError(Exception):
    """Custom exception for failures during AI content generation."""
    pass

class AIHandler:
    """A general-purpose handler for interacting with the Gemini 2.5 API."""

    def __init__(self, api_key: str, model: str, max_output_tokens: int, debug_mode: bool = False):
        if not api_key:
            raise ValueError("API key for the generative AI service is not set.")
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.debug_mode = debug_mode

    def _blocking_generate(self, prompt: str) -> str: # type: ignore [return]
        """A private, synchronous method that contains the actual blocking API call."""
        client = genai.Client()
        request_config = types.GenerateContentConfig(
            max_output_tokens=self.max_output_tokens,
            thinking_config=types.ThinkingConfig(thinking_budget=0),
        )

        try:
            # This is the critical point where we interact with the external service.
            response = client.models.generate_content(
                model=self.model,
                contents=[prompt],
                config=request_config
            )
            if self.debug_mode:
                print("\n--- Full API Response ---")
                print(response)
                print("-------------------------\n")
        except GoogleAPICallError as e:
            # Catch the specific library error and raise our own, cleaner exception.
            # This makes the rest of our application independent of the google-genai library's errors.
            raise AIGenerationError(f"The AI API call failed: {e}") from e
        except Exception as e:
            # Catch any other unexpected errors during the API call.
            raise AIGenerationError(f"An unexpected error occurred during AI generation: {e}") from e


    async def generate(self, prompt: str) -> str:
        """Generates content asynchronously by running the synchronous API call in a separate thread."""
        return await asyncio.to_thread(self._blocking_generate, prompt)