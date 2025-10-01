# lore_types.py

newType:
    # These should be new types for type safety and clarity
    entity_id: str
    turn: int
    # These ones I'm less sure about, but they could be useful
    primer: str
    personality: str
    memory: dict[turn = perspective]
    agents_intent: dict[entity_id = intention]
    # agents_perception: dict[entity_id = perception] # this is not relevant now, will be relevant much later.
    prompt_template: dict[key = fstr] # I donno how this works, we'll rework it when we get there, but it's supposed to be a multi-level dictionary of fstrings.
    agents: dict[entity_id = agent]

# Maybe these shared variables can be compacted somehow;
# separately: yes, these should be dataclasses or something.
class interaction:
    """Represents a basic interaction."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        content: str
    ):
        pass

class primer(interaction):
    """Represents a primer for an entity."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        personality: str,
        initial_perspective: str
    ):
        self.template = prompt_template.primer.agent

class intention(interaction):
    """Represents a user's intention within a specific turn."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        primer: str,
        formatted_memory: str
    ):
        self.template = prompt_template.intention

class initial_perspective(interaction):
    """Represents an initial perspective."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        primer: str,
        personality: str
    ):
        self.template = prompt_template.initial_perspective
        pass

class perspective(interaction):
    """Represents a perspective."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        primer: str,
        personality: str,
        reality_formatted: str
    ):
        self.template = prompt_template.perspective
        pass

class divination(interaction):
    """Represents a divination."""
    def __init__(
        self,
        owner: entity_id,
        turn_origin: turn,
        primer: str,
        reality_state: str,
        agents_intent_formatted: str
    ):
        self.template = prompt_template.divination
        pass
