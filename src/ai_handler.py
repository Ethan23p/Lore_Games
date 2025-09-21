import asyncio
import os
from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams
from . import config
from .prompts import PromptLibrary

# Create the application
fast = FastAgent("Lore_Games_AI")

@fast.agent(
  name="generator",
  instruction=PromptLibrary.TEMPLATES["primers"]["environment"],
  model="google.gemini-2.5-flash", # NOTE: Thisis the correct model name. - Ethan
  api_key=os.getenv("GEMINI_KEY"),
  request_params=RequestParams(
    maxTokens=config.MAX_TOKENS
  )
)
async def lore_agent():
    """
    This is a dummy function required by the @fast.agent decorator to register the agent.
    It is not called directly.
    """
    pass


class AIHandler:
    """
    A generic AI handler that uses the fast-agent library.
    """

    async def generate(self, prompt: str) -> str:
        """
        The core async logic to generate content using the fast-agent.
        """
        async with fast.run() as agent:
            response = await agent.generator.send(prompt)
            return response
