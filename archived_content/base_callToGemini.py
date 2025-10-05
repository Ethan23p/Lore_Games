from google import genai
from google.genai import types

client = genai.Client()

model = "gemini-2.5-flash"
max_tokens = 20
thinking = 0

response = client.models.generate_content(
    model=model,
    contents=["Provide a sizeable fun fact about the Roman empire"],
    config=types.GenerateContentConfig(
        max_output_tokens=20,
        thinking_config=types.ThinkingConfig(thinking_budget=thinking),
    )
)
print(response.text)
print("\n--- Full API Response ---")
print(response)
print("-------------------------\n")
