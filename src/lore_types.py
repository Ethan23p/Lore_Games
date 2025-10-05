# lore_types.py

from dataclasses import dataclass, field
from typing import TypeAlias, Dict, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities import Agent

# --- Core Type Aliases ---
EntityID: TypeAlias = str
Turn: TypeAlias = int

# --- Advanced Type Aliases ---
PrimerContent: TypeAlias = str
Personality: TypeAlias = str
Memory: TypeAlias = Dict[Turn, "Perspective"]
AgentsIntent: TypeAlias = Dict[EntityID, "Intention"]
Agents: TypeAlias = Dict[EntityID, "Agent"]
PromptTemplate = Dict[str, str | Dict[str, str]]

# --- Interaction Dataclasses ---

@dataclass(frozen=True, kw_only=True)
class BaseInteraction:
    owner: EntityID
    turn_origin: Turn

@dataclass(frozen=True, kw_only=True)
class Reality(BaseInteraction):
    content: str
    full_history: str

@dataclass(frozen=True, kw_only=True)
class BaseAIInteraction(BaseInteraction):
    content: str
    prompt: Optional[str] = None

@dataclass(frozen=True, kw_only=True)
class Intention(BaseAIInteraction):
    primer: PrimerContent
    formatted_memory: str
    template_key: str = field(default="agent.intent", init=False, repr=False)

@dataclass(frozen=True, kw_only=True)
class InitialPerspective(BaseAIInteraction):
    primer: PrimerContent
    personality: Personality
    template_key: str = field(default="env.prep_agent", init=False, repr=False)

@dataclass(frozen=True, kw_only=True)
class Perspective(BaseAIInteraction):
    primer: PrimerContent
    personality: Personality
    reality_formatted: str
    template_key: str = field(default="env.reflect", init=False, repr=False)

@dataclass(frozen=True, kw_only=True)
class Divination(BaseAIInteraction):
    primer: PrimerContent
    reality_state: str
    agents_intent_formatted: str
    template_key: str = field(default="env.divine", init=False, repr=False)