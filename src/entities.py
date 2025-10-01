# entities.py

from lore_types import (
    EntityID,
    Personality,
    Memory,
    Turn,
    Primer,
    Intention,
    InitialPerspective,
    Perspective,
    Divination,
    PerspectiveContent,
    IntentionContent,
)

class Agent:
    """Represents an autonomous entity within the simulation."""
    def __init__(self, id: EntityID, personality: Personality):
        self.id: EntityID = id
        self.personality: Personality = personality
        self.memory: Memory = {}

    def prime(self, initial_perspective: PerspectiveContent, current_turn: Turn) -> Primer:
        """Generates the agent's foundational primer."""
        pass

    def intent(self, current_turn: Turn) -> Intention:
        """Forms the agent's intention for the current turn."""
        pass

    def add_memory(self, turn: Turn, perspective: PerspectiveContent):
        """Adds a new perspective to the agent's memory."""
        self.memory[turn] = perspective

class Environment:
    """Represents the shared reality and orchestrates the simulation turns."""
    def __init__(self, id: EntityID, initial_reality: str):
        self.id: EntityID = id
        # Reality is a log of states, starting with the initial one.
        self.reality: dict[Turn, str] = {0: initial_reality}
        self.agents_intent: dict[EntityID, IntentionContent] = {}

    def initial_reflection(
        self, agent_id: EntityID, agent_personality: Personality, turn_current: Turn
    ) -> InitialPerspective:
        """Generates the request for an agent's first look at the world."""
        pass

    def reflect(
        self, agent_id: EntityID, personality: Personality, turn: Turn
    ) -> Perspective:
        """Generates the request for an agent's perspective on the current reality."""
        pass

    def add_intention(self, agent_id: EntityID, intention: IntentionContent, turn: Turn):
        """Records an agent's intention for a given turn."""
        self.agents_intent[agent_id] = intention

    def divine(self, current_turn: Turn) -> Divination:
        """
        Asks the simulation to interpret the combined intentions
        and produce the next state of reality.
        """
        pass