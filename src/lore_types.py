from typing import NewType, Dict, List, Optional
from uuid import UUID, uuid4
from src.ai_handler import AIHandler
from src.prompt_templates import PROMPT_TEMPLATES
from src.state_logger import StateLogger

# --- Core Types ---

AgentId = NewType('AgentId', UUID)
TurnId = NewType('TurnId', int)

# --- Interaction Taxonomy ---

class Interaction:
    """The base structure for all events and communications."""
    def __init__(self, owner: AgentId, birth_turn: TurnId, content: str):
        self.owner = owner
        self.birth_turn = birth_turn
        self.content = content

class Perception(Interaction):
    """An agent's observation of reality."""
    pass

class Introspection(Interaction):
    """An agent's internal thoughts."""
    pass

class Intention(Interaction):
    """An agent's desired action."""
    pass

class Action(Interaction):
    """An agent's action as realized by the environment."""
    pass

class Divination(Interaction):
    """The environment's description of the state of reality."""
    pass

# --- Entity Taxonomy ---

class Entity:
    """Base class for all game objects."""
    pass

class Agent(Entity):
    """An autonomous entity capable of thought and action."""
    def __init__(self, name: str, personality: str, ai_handler: AIHandler, logger: Optional[StateLogger] = None):
        self.id: AgentId = AgentId(uuid4())
        self.name: str = name
        self.personality: str = personality
        self.ai: AIHandler = ai_handler
        self.logger = logger
        self.memory: List[Introspection] = []

    def introspect(self, perception: Perception) -> Introspection:
        """Generates an internal monologue based on perception."""
        template = PROMPT_TEMPLATES["AGENT_INTROSPECT"]
        prompt = template.format(
            name=self.name,
            personality=self.personality,
            memory=[mem.content for mem in self.memory],
            perception=perception.content
        )
        if self.logger:
            self.logger.log_prompt(f"agent_{self.name}_introspect.md", prompt)
        ai_content = self.ai.generate(prompt)

        new_introspection = Introspection(
            owner=self.id,
            birth_turn=perception.birth_turn,
            content=ai_content
        )
        self.memory.append(new_introspection)
        return new_introspection

    def intent(self, perception: Perception) -> Intention:
        """Forms a concrete intention based on internal state."""
        template = PROMPT_TEMPLATES["AGENT_INTENT"]
        prompt = template.format(
            name=self.name,
            personality=self.personality,
            memory=[mem.content for mem in self.memory],
            perception=perception.content
        )
        if self.logger:
            self.logger.log_prompt(f"agent_{self.name}_intent.md", prompt)
        ai_content = self.ai.generate(prompt)

        return Intention(
            owner=self.id,
            birth_turn=perception.birth_turn,
            content=ai_content
        )

    def run_turn(self, perception: Perception) -> Intention:
        """Encapsulates the agent's full turn logic."""
        self.introspect(perception)
        intention = self.intent(perception)
        return intention

class Environment(Entity):
    """The context in which agents exist and interact."""
    def __init__(self, agents: List[Agent], initial_reality: str, ai_handler: AIHandler, logger: Optional[StateLogger] = None):
        self.id: AgentId = AgentId(UUID(int=0)) # Special ID for the environment
        self.agents = agents
        self.agent_map = {agent.id: agent for agent in agents}
        self.ai: AIHandler = ai_handler
        self.logger = logger

        initial_divination = Divination(
            owner=self.id,
            birth_turn=TurnId(-1),
            content=initial_reality
        )
        self.reality: List[Divination] = [initial_divination]

    def physics(self, intention: Intention) -> Action:
        """Determines the conceivable outcome of an agent's intention."""
        template = PROMPT_TEMPLATES["ENV_PHYSICS"]
        prompt = template.format(
            agent_name=self.agent_map[intention.owner].name,
            intention_content=intention.content
        )
        if self.logger:
            self.logger.log_prompt("environment_physics.md", prompt)
        ai_content = self.ai.generate(prompt)

        return Action(
            owner=intention.owner,
            birth_turn=intention.birth_turn,
            content=ai_content
        )

    def divination(self, turn: TurnId, actions: List[Action]):
        """Describes the new state of reality based on all actions."""
        turn_events_str = '; '.join([f"{self.agent_map[a.owner].name} {a.content}" for a in actions])
        template = PROMPT_TEMPLATES["ENV_DIVINATION"]
        prompt = template.format(turn_events=turn_events_str)
        if self.logger:
            self.logger.log_prompt("environment_divination.md", prompt)
        ai_content = self.ai.generate(prompt)

        new_divination = Divination(
            owner=self.id,
            birth_turn=turn,
            content=ai_content
        )
        self.reality.append(new_divination)

    def reflect(self, agent: Agent, turn: TurnId) -> Perception:
        """Generates a perception from the history of reality."""
        narrative_history = [div.content for div in self.reality]
        perception_content = " ".join(narrative_history)

        return Perception(
            owner=agent.id,
            birth_turn=turn,
            content=perception_content
        )

    def run_turn(self, turn: TurnId):
        """Runs a full turn of the simulation."""
        all_intentions: List[Intention] = []

        for agent in self.agents:
            perception = self.reflect(agent, turn)
            intention = agent.run_turn(perception)
            all_intentions.append(intention)

        all_actions: List[Action] = []
        for intention in all_intentions:
            action = self.physics(intention)
            all_actions.append(action)

        self.divination(turn, all_actions)
