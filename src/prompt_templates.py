# src/prompt_templates.py

"""
Central repository for all AI prompt templates used in the simulation.
Using a central location makes it easier to manage and tune the AI's
voice and instructions.
"""

PROMPT_TEMPLATES = {
    "AGENT_INTROSPECT": (
        "I'm {name}, people say I'm {personality}. "
        "What has happened so far: {memory}. "
        "What just happened is {perception}. "
        "Now I'm considering the overall situation, especially considering the latest happenings. "
        "My thoughts are this:"
    ),
    
    "AGENT_INTENT": (
        "I am {name} ({personality}). My internal monologue and memory is: "
        "{memory}. "
        "The current reality I perceive is: {perception}. "
        "Based on my thoughts and the situation, I will now form a concrete plan. "
        "My intention is to:"
    ),
    
    "ENV_PHYSICS": (
        "An agent, {agent_name}, has declared their intention to: '{intention_content}'. "
        "Describe the most plausible, immediate, and physically conceivable outcome of this action "
        "in a single, objective sentence."
    ),
    
    "ENV_DIVINATION": (
        "The following events occurred this turn: {turn_events}. "
        "Synthesize these events into a single, cohesive narrative paragraph describing the new "
        "state of reality from a third-person, objective perspective."
    )
}
