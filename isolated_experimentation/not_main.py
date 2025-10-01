from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model=config.ai.model,
    contents=["Foobar?"],
    config=types.GenerateContentConfig(
        max_output_tokens=ai.config.max_outputTokens,
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )
)
print(response.text)