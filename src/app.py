# app.py

import asyncio
from typing import Optional, Coroutine, TypeVar, Any

from config import get_config
from ai_handler import AIHandler
from lore_types import Agents, Turn, BaseInteraction, Reality
from entities import Agent, Environment
from prompts import PROMPT_TEMPLATES
from chronicle import Chronicle

T = TypeVar('T', bound=BaseInteraction)

class LoreGamesApp:
    """The central orchestrator for the Lore Games simulation."""

    def __init__(self):
        self.config = get_config()
        self.ai_handler = AIHandler(
            api_key=self.config["ai"]["api_key"],
            model=self.config["ai"]["model"],
            max_output_tokens=self.config["ai"]["max_output_tokens"],
            debug_mode=self.config["simulation"]["debug_mode"]
        )
        self.prompts = PROMPT_TEMPLATES
        self.chronicle = Chronicle(config=self.config["simulation"], base_path="state_dump")
        self.agents: Agents = {}
        self.environment: Optional[Environment] = None
        self.current_turn: Turn = 0

    def setup(self):
        self.chronicle.log_setup_start()
        for name, agent_config in self.config["initial_agents"].items():
            new_agent = Agent(id=name, personality=agent_config["personality"], ai_handler=self.ai_handler, prompts=self.prompts)
            self.agents[name] = new_agent
            self.chronicle.log_agent_creation(name)
        env_config = self.config["environment"]
        self.environment = Environment(id=env_config["id"], initial_reality=env_config["initial_reality"], ai_handler=self.ai_handler, prompts=self.prompts)
        self.chronicle.log_environment_creation(self.environment.id)
        self.chronicle.log_setup_end()

    async def _prime_agents(self):
        assert self.environment is not None
        self.chronicle.log_priming_start()
        for agent in self.agents.values():
            initial_perspective = await self.chronicle.execute_and_log(self.environment.initial_reflection(agent, self.current_turn))
            agent.prime(initial_perspective)
        self.chronicle.log_priming_end()

    async def _execute_turn(self):
        assert self.environment is not None
        self.current_turn += 1
        reality_str = self.environment.reality.get(self.current_turn - 1, "")
        self.chronicle.log_turn_start(self.current_turn, reality_str)

        for agent in self.agents.values():
            perspective = await self.chronicle.execute_and_log(self.environment.reflect(agent, self.current_turn))
            agent.add_memory(self.current_turn, perspective)
            intention = await self.chronicle.execute_and_log(agent.intent(self.current_turn))
            self.environment.add_intention(agent.id, intention)

        divination = await self.chronicle.execute_and_log(self.environment.divine(self.current_turn))
        self.environment.reality[self.current_turn] = divination.content

        final_reality = Reality(owner=self.environment.id, turn_origin=self.current_turn, content=divination.content)
        self.chronicle.log(final_reality)
        self.chronicle.log_turn_end()

    async def run(self):
        """The main application loop."""
        self.setup()
        await self._prime_agents()
        while True:
            user_input = input("\nPress Enter to advance to the next turn (or type 'quit' to exit)...")
            if user_input.lower() == 'quit':
                break
            await self._execute_turn()
