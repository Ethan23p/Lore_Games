# app.py

import asyncio
from typing import Optional, Coroutine, TypeVar, Any

from config import get_config
from ai_handler import AIHandler, AIGenerationError
from lore_types import Agents, Turn, BaseInteraction, Reality
from entities import Agent, Environment
from prompts import PROMPT_TEMPLATES
from chronicle import Chronicle

T = TypeVar('T', bound=BaseInteraction)

class LoreGamesApp:
    """The central orchestrator for the Lore Games simulation."""

    def __init__(self):
        self.config = get_config()
        self.ai_handler = AIHandler(api_key=self.config["ai"]["api_key"], model=self.config["ai"]["model"], max_output_tokens=self.config["ai"]["max_output_tokens"])
        self.prompts = PROMPT_TEMPLATES
        self.chronicle = Chronicle(base_path="state_dump")
        self.agents: Agents = {}
        self.environment: Optional[Environment] = None
        self.current_turn: Turn = 0

    async def _execute_and_log(self, interaction_coro: Coroutine[Any, Any, T]) -> T:
        """Awaits an interaction coroutine, logs it, and returns the result."""
        try:
            result = await interaction_coro
            self.chronicle.log(result)
            return result
        except AIGenerationError as e:
            print(f"FATAL: An AI generation error occurred: {e}")
            raise

    def setup(self):
        # ... (setup method remains the same) ...
        print("--- Initializing Simulation ---")
        for name, agent_config in self.config["initial_agents"].items():
            new_agent = Agent(id=name, personality=agent_config["personality"], ai_handler=self.ai_handler, prompts=self.prompts)
            self.agents[name] = new_agent
            print(f"Created agent: {name}")
        env_config = self.config["environment"]
        self.environment = Environment(id=env_config["id"], initial_reality=env_config["initial_reality"], ai_handler=self.ai_handler, prompts=self.prompts)
        print(f"Created environment: {self.environment.id}")
        print("-----------------------------")

    async def _prime_agents(self):
        assert self.environment is not None
        print("\n--- Priming Agents (Turn 0) ---")
        for agent in self.agents.values():
            initial_perspective = await self._execute_and_log(self.environment.initial_reflection(agent, self.current_turn))
            agent.prime(initial_perspective)
            print(f"Primed {agent.id}.")
        print("---------------------------------")

    async def _execute_turn(self):
        assert self.environment is not None
        self.current_turn += 1
        print(f"\n--- Starting Turn {self.current_turn} ---")
        print(f"Reality: {self.environment.reality.get(self.current_turn - 1)}")
        for agent in self.agents.values():
            perspective = await self._execute_and_log(self.environment.reflect(agent, self.current_turn))
            agent.add_memory(self.current_turn, perspective)
            print(f"{agent.id} perceives: \"{perspective.content[:80].strip()}...\"")
            intention = await self._execute_and_log(agent.intent(self.current_turn))
            self.environment.add_intention(agent.id, intention)
            print(f"{agent.id} intends: \"{intention.content[:80].strip()}...\"")
        divination = await self._execute_and_log(self.environment.divine(self.current_turn))
        self.environment.reality[self.current_turn] = divination.content
        final_reality = Reality(owner=self.environment.id, turn_origin=self.current_turn, content=divination.content)
        self.chronicle.log(final_reality)
        print(f"\nNew Reality: {divination.content}")
        print("--- End of Turn ---")

    async def run(self):
        """The main application loop."""
        self.setup()
        await self._prime_agents()
        while True:
            user_input = input("\nPress Enter to advance to the next turn (or type 'quit' to exit)...")
            if user_input.lower() == 'quit':
                break
            await self._execute_turn()