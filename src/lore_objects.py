from __future__ import annotations
from .ai_handler import AIHandler
from typing import List, Dict, Optional
from . import config
import os

class PromptLibrary:
    """
    A library of prompt templates for the simulation.
    """

    TEMPLATES = {
        "Perspective": "Given {reality}, what does {agent_name} perceive at this moment?",
        "Introspection": (
            "You are {agent_name}, you've been described as {personality}.\n"
            "Your memory of what has happened so far: {memory}\n"
            "What you have noticed recently: {perception}\n"
            "Consider these latest events, private matters, your motivations. "
            "What do you want to add to your memory?"
        ),
        "Intention": (
            "You are {agent_name}, you've been described as {personality}.\n"
            "What has happened so far: {memory}\n"
            "What you've noticed recently: {perception}\n"
            "What do you *intend* to do next, in the physical realm? "
            "If your intent is conceivable, you will attempt to execute; "
            "be mindful that if your intent is not possible, you will "
            "effectively do nothing at all."
        ),
        "Action": "Given {reality}, can {intent_owner} do {intent}?",
        "Divination": (
            "Given {reality} and the agents' intention to do the following, "
            "what happens next? {agents_actions}"
        ),
    }


def _log_interaction(interaction):

    """
    Logs the details of an interaction to a file, overwriting fleeting states
    and appending to continuous states.
    """
    if not config.LOGGING_ENABLED:
        return

    interaction_type = interaction.__class__.__name__
    fleeting_states = ["Perspective", "Intention", "Action"]
    continuous_states = ["Introspection", "Divination"]

    # Determine the file path and mode
    if interaction_type in fleeting_states or interaction_type in continuous_states:
        log_dir = os.path.join(".state_dump", interaction.owner)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        filepath = os.path.join(log_dir, f"{interaction_type}.md")
        file_mode = "w" if interaction_type in fleeting_states else "a"
    else:
        # Do not log interactions that are not explicitly categorized.
        return

    # Format the content for the log file
    content = (
        f"# Turn {interaction.birth_turn}\n\n"
        f"## Prompt\n\n```\n{interaction.prompt}\n```\n\n"
        f"## Content\n\n```\n{interaction.content}\n```\n"
        f"---"
    )

    with open(filepath, file_mode) as f:
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

    print(f"[TURN {turn} | {owner} | {interaction_type}] -> \"{content}\"")


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

    def generate(self, **kwargs):
        """
        Generates content using the AI handler and logs the interaction.
        """
        self._create_prompt(**kwargs)
        self.content = self.ai_handler.generate(self.prompt)
        _log_interaction(self)
        _debug_print(self)
        return self.content




class Perspective(Interaction):
    """
    Represents the perspective of an agent.
    """

    def __init__(self, owner: str, birth_turn: int, ai_handler: AIHandler):
        prompt_template = PromptLibrary.TEMPLATES["Perspective"]
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
        prompt_template = PromptLibrary.TEMPLATES["Introspection"]
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
        prompt_template = PromptLibrary.TEMPLATES["Intention"]
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
        prompt_template = PromptLibrary.TEMPLATES["Action"]
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
        prompt_template = PromptLibrary.TEMPLATES["Divination"]
        super().__init__(owner, birth_turn, ai_handler, prompt_template)

    def _create_prompt(self, reality: str, agents_actions: str, **kwargs):
        self.prompt = self._prompt_template.format(
            reality=reality, agents_actions=agents_actions
        )




class Agent:
    """
    Represents an agent in the simulation.
    """

    def __init__(self, agent_name: str, personality: str, ai_handler: AIHandler):
        self.agent_name = agent_name
        self.personality = personality
        self.ai_handler = ai_handler
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

    def introspect(self, birth_turn: int) -> Introspection:
        """
        Integrate latest events, consider private matters, consider motivations, consider personality.
        """
        introspection = Introspection(
            owner=self.agent_name, birth_turn=birth_turn, ai_handler=self.ai_handler
        )
        memory_str = "\n".join([i.content for i in self.memory])
        perception_str = self.perception.content if self.perception else ""
        introspection.generate(
            agent_name=self.agent_name,
            personality=self.personality,
            memory=memory_str,
            perception=perception_str,
        )
        self.memory.append(introspection)
        return introspection

    def intend(self, birth_turn: int) -> Intention:
        """
        Put forward intention within the physical, simulated realm.
        """
        intention = Intention(
            owner=self.agent_name, birth_turn=birth_turn, ai_handler=self.ai_handler
        )
        memory_str = "\n".join([i.content for i in self.memory])
        perception_str = self.perception.content if self.perception else ""
        intention.generate(
            agent_name=self.agent_name,
            personality=self.personality,
            memory=memory_str,
            perception=perception_str,
        )
        return intention


class Environment:
    """
    Represents the simulation environment.
    """

    def __init__(self, ai_handler: AIHandler, initial_reality: str):
        self.ai_handler = ai_handler
        self.initial_reality = initial_reality
        self.reality: List[Divination] = []
        self.agents_intentions: Dict[str, Intention] = {}
        self.agents_actions: Dict[str, Action] = {}
        self.turn = 0

    def physics(self, intention: Intention) -> Action:
        """
        Simply evaluate if stated intention is conceivable or not.
        """
        action = Action(
            owner=intention.owner, birth_turn=self.turn, ai_handler=self.ai_handler
        )
        reality_str = self.reality[-1].content if self.reality else self.initial_reality
        
        # Dummy logic: for now, all intentions are possible
        is_possible = True

        if is_possible:
            action.generate(reality=reality_str, intent_owner=intention.owner, intent=intention.content)
        else:
            action.content = "does nothing."
        
        self.agents_actions[intention.owner] = action
        return action

    def divine(self) -> Divination:
        """
        Taking into consideration all agents' intentions in equal parts, what happens next.
        """
        divination = Divination(
            owner="environment", birth_turn=self.turn, ai_handler=self.ai_handler
        )
        reality_str = self.reality[-1].content if self.reality else self.initial_reality
        actions_str = "\n".join(
            [f"{owner}: {action.content}" for owner, action in self.agents_actions.items()]
        )
        divination.generate(reality=reality_str, agents_actions=actions_str)
        self.reality.append(divination)
        return divination

    def reflect(self, agent_name: str) -> Perspective:
        """
        Considering the state of the environment, what would the agent perceive.
        """
        perspective = Perspective(
            owner=agent_name, birth_turn=self.turn, ai_handler=self.ai_handler
        )
        reality_str = self.reality[-1].content if self.reality else self.initial_reality
        perspective.generate(reality=reality_str, agent_name=agent_name)
        return perspective


    def advance_turn(self, agents: List["Agent"]):
        """
        Runs a single turn of the simulation.
        """
        # Agents introspect and intend
        for agent in agents:
            agent.introspect(self.turn)
            intention = agent.intend(self.turn)
            self.agents_intentions[agent.agent_name] = intention

        # Environment processes intentions into actions
        for agent_name, intention in self.agents_intentions.items():
            self.physics(intention)

        # Environment divines the outcome of the turn
        self.divine()

        # Agents perceive the new reality
        for agent in agents:
            perspective = self.reflect(agent.agent_name)
            agent.perceive(perspective)
