from __future__ import annotations
from .ai_handler import AIHandler
from typing import List, Dict, Optional, Mapping
from . import config
import os
import asyncio
from .prompts import PromptLibrary


def _log_interaction(interaction):
    """
    Logs the details of an interaction to a file, overwriting fleeting states
    and appending to continuous states.
    """
    if not config.LOGGING_ENABLED:
        return

    interaction_map = {
        "Intention": "Intent.md",
        "Introspection": "Memory.md",
        "Divination": "Reality.md",
    }
    
    description_map = {
        "Intention": "This file contains the agent's intended action for the current turn.",
        "Introspection": "This file contains the complete, evolving memory of the agent.",
        "Divination": "This file contains the official, shared reality of the simulation.",
    }

    interaction_type = interaction.__class__.__name__
    if interaction_type not in interaction_map:
        return

    log_filename = interaction_map[interaction_type]
    fleeting_states = ["Intention"]
    
    # Determine the file path and mode
    log_dir = os.path.join(".state_dump", interaction.owner)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    filepath = os.path.join(log_dir, log_filename)
    file_mode = "w" if interaction_type in fleeting_states else "a"

    # Add a header only if the file is new (or being overwritten)
    header = ""
    if file_mode == "w" or not os.path.exists(filepath):
        header = f"# {interaction.owner}'s {interaction_type}\n\n> {description_map[interaction_type]}\n\n---\n\n"

    # Format the content for the log file
    content = (
        f"## Turn {interaction.birth_turn}\n\n"
        f"{interaction.content}\n\n"
        f"### Prompt\n\n"
        f"```\n{interaction.prompt}\n```\n\n"
        f"---\n\n"
    )

    with open(filepath, file_mode, encoding='utf-8') as f:
        if header:
            f.write(header)
        f.write(content)


def _debug_print(interaction):
    """
    Prints a concise summary of an interaction to the console for debugging.
    """
    if not config.DEBUG_PRINTING_ENABLED:
        return

    interaction_type = interaction.__class__.__name__
    owner = interaction.owner
    turn = interaction.birth_turn
    content = interaction.content.strip()
    
    first_line = content.split('\n')[0]
    if len(content) > len(first_line):
        first_line += "..."

    print(f"[TURN {turn} | {owner} | {interaction_type}] -> \"{first_line}\"")


class Interaction:
    """
    Base class for all interactions.
    """


    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler, prompt_template: str = ""):
        self.owner = owner
        self.birth_turn = birth_turn
        self._prompt_template = prompt_template
        self.prompt = ""
        self.content = ""
        self.ai_handler = ai_handler

    def _create_prompt(self, *args, **kwargs):
        """
        Creates the prompt from the template.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError

    async def generate(self, **kwargs):
        """
        Generates content using the AI handler and logs the interaction.
        """
        self._create_prompt(**kwargs)
        self.content = await self.ai_handler.generate(self.prompt)

        if not self.content or not self.content.strip():
            print("\n[SYSTEM WARNING] The AI returned an empty response.")
            print("This may be due to the MAX_TOKENS setting in src/config.py being too low for the current prompt.")
            await asyncio.to_thread(input, "Press Enter to continue the simulation...")

        _log_interaction(self)
        _debug_print(self)
        return self.content




class Perspective(Interaction):
    """
    Represents the perspective of an agent.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["main_flow"]["perspective"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(self, reality: str, agent_name: str, **kwargs):
        self.prompt = self._prompt_template.format(
            reality=reality, agent_name=agent_name
        )


class Perception(Interaction):
    """
    Represents what an agent perceives.
    This is typically the result of a Perspective interaction.
    """

    def __init__(self, owner: str, birth_turn: int, content: str, ai_handler: AIHandler):
        super().__init__(owner, birth_turn, ai_handler)
        self.content = content


class Introspection(Interaction):
    """
    Represents an agent's introspection.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["main_flow"]["introspection"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(
        self,
        agent_name: str,
        personality: str,
        memory: str,
        perception: str,
        **kwargs,
    ):
        self.prompt = self._prompt_template.format(
            agent_name=agent_name,
            personality=personality,
            memory=memory,
            perception=perception,
        )


class Intention(Interaction):
    """
    Represents an agent's intention.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["main_flow"]["intention"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(
        self,
        agent_name: str,
        personality: str,
        memory: str,
        perception: str,
        **kwargs,
    ):
        self.prompt = self._prompt_template.format(
            agent_name=agent_name,
            personality=personality,
            memory=memory,
            perception=perception,
        )


class Action(Interaction):
    """
    Represents an agent's action.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["main_flow"]["action"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(self, reality: str, intent_owner: str, intent: str, **kwargs):
        self.prompt = self._prompt_template.format(
            reality=reality, intent_owner=intent_owner, intent=intent
        )


class Divination(Interaction):
    """
    Represents the outcome of a turn.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["main_flow"]["divination"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(self, reality: str, agents_intent: str, **kwargs):
        self.prompt = self._prompt_template.format(
            reality=reality, agents_intent=agents_intent
        )


class Plan(Interaction):
    """
    Represents an agent's plan for the turn in the simple flow.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["simple_flow"]["planning"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(self, reality: str, **kwargs):
        self.prompt = self._prompt_template.format(reality=reality)




class Agent:
    """
    Represents an agent in the simulation.
    """

    def __init__(self, agent_name: str, personality: str, ai_handler: AIHandler):
        self.agent_name = agent_name
        self.personality = personality
        self.ai_handler = ai_handler
        self.primer = PromptLibrary.TEMPLATES["primers"]["agent"].format(
            agent_name=agent_name, personality=personality
        )
        self.memory: List[Introspection] = []
        self.perception: Optional[Perception] = None

    def perceive(self, perspective: Perspective) -> Perception:
        """
        Blindly accept currently primed perspective.
        """
        self.perception = Perception(
            owner=self.agent_name,
            birth_turn=perspective.birth_turn,
            content=perspective.content,
            ai_handler=self.ai_handler,
        )
        return self.perception

    async def introspect(self, birth_turn: int) -> Introspection:
        """
        Integrate latest events, consider private matters, consider motivations, consider personality.
        """
        introspection = Introspection(
            owner=self.agent_name, birth_turn=birth_turn, ai_handler=self.ai_handler
        )
        memory_content = "\n".join([i.content for i in self.memory])
        perception_content = self.perception.content if self.perception else ""
        await introspection.generate(
            agent_name=self.agent_name,
            personality=self.personality,
            memory=memory_content,
            perception=perception_content,
        )
        self.memory.append(introspection)
        return introspection

    async def intend(self, birth_turn: int) -> Intention:
        """
        Put forward intention within the physical, simulated realm.
        """
        intention = Intention(
            owner=self.agent_name, birth_turn=birth_turn, ai_handler=self.ai_handler
        )
        memory_content = "\n".join([i.content for i in self.memory])
        perception_content = self.perception.content if self.perception else ""
        await intention.generate(
            agent_name=self.agent_name,
            personality=self.personality,
            memory=memory_content,
            perception=perception_content,
        )
        return intention

    async def plan(self, birth_turn: int, reality: str) -> Plan:
        """
        Generate a plan for the turn based on the current reality.
        """
        plan = Plan(
            owner=self.agent_name, birth_turn=birth_turn, ai_handler=self.ai_handler
        )
        await plan.generate(reality=reality)
        return plan


class Environment:
    """
    Represents the simulation environment.
    """

    def __init__(self, ai_handler: AIHandler, initial_reality: str):
        self.ai_handler = ai_handler
        self.initial_reality = initial_reality
        self.primer = PromptLibrary.TEMPLATES["primers"]["environment"]
        self.reality: List[Divination] = []
        self.agents_intentions: Dict[str, Intention] = {}
        self.agents_actions: Dict[str, Action] = {}
        self.agents_plans: Dict[str, Plan] = {}
        self.turn = 0


    async def physics(self, intention: Intention) -> Action:
        """
        Simply evaluate if stated intention is conceivable or not.
        """
        action = Action(
            owner=intention.owner, birth_turn=self.turn, ai_handler=self.ai_handler
        )
        current_reality = self.reality[-1].content if self.reality else self.initial_reality

        # Dummy logic: for now, all intentions are possible
        is_possible = True

        if is_possible:
            await action.generate(reality=current_reality, intent_owner=intention.owner, intent=intention.content)
        else:
            action.content = "does nothing."

        self.agents_actions[intention.owner] = action
        return action

    async def divine(self, agents_intent: Mapping[str, Interaction]) -> Divination:
        """
        Taking into consideration all agents' intentions in equal parts, what happens next.
        """
        divination = Divination(
            owner="environment", birth_turn=self.turn, ai_handler=self.ai_handler
        )
        current_reality = self.reality[-1].content if self.reality else self.initial_reality
        formatted_intents = "\n".join(
            [f"{owner}: {agent_intent.content}" for owner, agent_intent in agents_intent.items()]
        )
        await divination.generate(reality=current_reality, agents_intent=formatted_intents)
        self.reality.append(divination)
        return divination

    async def reflect(self, agent_name: str) -> Perspective:
        """
        Considering the state of the environment, what would the agent perceive.
        """
        perspective = Perspective(
            owner=agent_name, birth_turn=self.turn, ai_handler=self.ai_handler
        )
        current_reality = self.reality[-1].content if self.reality else self.initial_reality
        await perspective.generate(reality=current_reality, agent_name=agent_name)
        return perspective