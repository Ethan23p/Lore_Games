# config.py

"""
Central configuration for the Lore Games simulation.
"""
import os
from typing import Dict, Any, List

_AGENTS_LIST: List[Dict[str, str]] = [
    {
        "name": "Charlie",
        "personality": "A goblin which once survived being thrown into a ceremonial bonfire; Charlie has a new appreciation for life.",
    },
    {
        "name": "Delta",
        "personality": "A mechanoid which speaks through a lo-fi speaker, Delta is fascinated by biology.",
    },
]

INITIAL_AGENTS: Dict[str, Dict[str, str]] = {
    agent['name']: agent for agent in _AGENTS_LIST
}

def get_config() -> Dict[str, Any]:
    """Returns the main configuration dictionary for the simulation."""

    config: Dict[str, Any] = {
        "simulation": {
            "write_to_file": True,
            "print_to_cmd": True,
            "debug_mode": False,
            "flow": "simple",
        },
        "ai": {
            "max_output_tokens": 556,
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "model": "gemini-2.5-flash", # 2.5 is absolutely intentional, don't change it.
        },
        "initial_agents": INITIAL_AGENTS,
        "environment": {
            "id": "environment",
            "initial_reality": "A sprawling shantytown built on the interconnected rooftops of a sleeping city; residents of 'Grimward' are compressed into each other as a population of demons seep into the city. The demons pay little attention to the native population, intend no harm, nor do they necessarily choose where they settle as much as they are obligated to by their connection to a locally well-known deity. Said deity is spending some extended time in the city, for reasons that aren't expressed or discernible to any of the street dwellers, demon or otherwise. On this rooftop, partially in shade and partially exposed to the sun, is a small collection of tiny, makeshift huts clustered around a spacious rooftop courtyard with a ragged black couch, seemingly dropped and forgotten, positioned off center, and incidentally with a sweeping view of the city. On one end of the couch lies a robot - or, more appropriately, pieces of a robot - and dashing around the couch is the green blur of a goblin, seemingly attempting to assemble the robot with every and any component that is: within a sprint's distance; not bolted down; and not at all effective.",
        },
    }

    return config
