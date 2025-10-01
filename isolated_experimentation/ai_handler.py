from google import genai
from google.genai import types

class AIHandler:
    def __init__(self, api_key: str, model: str, max_outputTokens: int):
        if not api_key:
            raise ValueError("API key for the generative AI service is not set.")

    async def generate(self, prompt: str) -> str:

        client = genai.Client()

        response = client.models.generate_content(
            model=config.ai.model,
            contents=["Foobar?"],
            config=types.GenerateContentConfig(
                max_output_tokens=config.ai.max_outputTokens,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            )
        )
        print(response.text)