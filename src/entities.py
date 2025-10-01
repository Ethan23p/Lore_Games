# entities.py

from typing import Dict, Any
import textwrap
from dataclasses import replace

from ai_handler import AIHandler
from lore_types import (
    EntityID, Personality, Memory, Turn, Intention, InitialPerspective,
    Perspective, Divination, PrimerContent, AgentsIntent
)

def _format_prompt(prompts: Dict, template_key: str, data: Any) -> str:
    """A helper utility to format a prompt from the templates dictionary."""
    key1, key2 = template_key.split('.')
    template = prompts[key1][key2]
    return textwrap.dedent(template).strip().format(**data.__dict__)

class Agent:
    """Represents an autonomous entity that can perceive, reason, and act."""
    def __init__(self, id: EntityID, personality: Personality, ai_handler: AIHandler, prompts: Dict):
        self.id: EntityID = id
        self.personality: Personality = personality
        self.primer: PrimerContent = ""
        self.memory: Memory = {}
        self.ai_handler = ai_handler
        self.prompts = prompts

    def prime(self, initial_perspective: InitialPerspective) -> None:
        """Generates and stores the agent's foundational primer."""
        self.primer = textwrap.dedent(f"""
            <ROLE>
                You are {self.id}, you are described like this: {self.personality}.

                You recall your earlier perspective:

                {initial_perspective.content}.
            <ROLE END>
        """).strip()

    async def intent(self, current_turn: Turn) -> Intention:
        """Forms and returns the agent's full intention interaction."""
        formatted_memory = "\n".join(
            f"Turn {t}: {p.content}" for t, p in self.memory.items()
        )
        request = Intention(
            owner=self.id,
            turn_origin=current_turn,
            primer=self.primer,
            formatted_memory=formatted_memory,
            content=""
        )
        prompt = _format_prompt(self.prompts, request.template_key, request)
        response = await self.ai_handler.generate(prompt)
        return replace(request, content=response, prompt=prompt)

    def add_memory(self, turn: Turn, perspective: Perspective):
        """Adds a new perspective object to the agent's memory."""
        self.memory[turn] = perspective

class Environment:
    """Represents the shared reality and orchestrates simulation turns."""
    def __init__(self, id: EntityID, initial_reality: str, ai_handler: AIHandler, prompts: Dict):
        self.id: EntityID = id
        self.primer: PrimerContent = textwrap.dedent(prompts["env"]["primer"]).strip()
        self.reality: dict[Turn, str] = {0: initial_reality}
        self.agents_intent: AgentsIntent = {}
        self.ai_handler = ai_handler
        self.prompts = prompts

    async def initial_reflection(self, agent: "Agent", turn_current: Turn) -> InitialPerspective:
        """Generates an agent's first look at the world."""
        request = InitialPerspective(
            owner=agent.id,
            turn_origin=turn_current,
            primer=self.primer,
            personality=agent.personality,
            content=""
        )
        prompt = _format_prompt(self.prompts, request.template_key, request)
        response = await self.ai_handler.generate(prompt)
        return replace(request, content=response, prompt=prompt)

    async def reflect(self, agent: "Agent", turn: Turn) -> Perspective:
        """Generates an agent's perspective on the current reality."""
        current_reality = self.reality.get(turn - 1, "A formless void.")
        request = Perspective(
            owner=agent.id,
            turn_origin=turn,
            primer=self.primer,
            personality=agent.personality,
            reality_formatted=current_reality,
            content=""
        )
        prompt = _format_prompt(self.prompts, request.template_key, request)
        response = await self.ai_handler.generate(prompt)
        return replace(request, content=response, prompt=prompt)

    def add_intention(self, agent_id: EntityID, intention: Intention):
        """Records an agent's intention object for a given turn."""
        self.agents_intent[agent_id] = intention

    async def divine(self, current_turn: Turn) -> Divination:
        """Interprets intentions and produces the next state of reality."""
        reality_state = self.reality.get(current_turn - 1, "A formless void.")
        agents_intent_formatted = "\n".join(
            f"Agent {id}'s intention: {intent.content}" for id, intent in self.agents_intent.items()
        )
        request = Divination(
            owner=self.id,
            turn_origin=current_turn,
            primer=self.primer,
            reality_state=reality_state,
            agents_intent_formatted=agents_intent_formatted,
            content=""
        )
        prompt = _format_prompt(self.prompts, request.template_key, request)
        response = await self.ai_handler.generate(prompt)
        return replace(request, content=response, prompt=prompt)