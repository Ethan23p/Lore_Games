# config.py

"""
Central configuration for the Lore Games simulation.
"""
import os
from typing import Dict, Any, List

_AGENTS_LIST: List[Dict[str, str]] = [
    {
        "name": "Charlie",
        "personality": "A goblin which survived being thrown into a ceremonial bonfire; Charlie has a new appreciation for life.",
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
            "max_output_tokens": 20,
            "api_key": os.environ.get("GEMINI_API_KEY"),
            "model": "gemini-2.5-flash", # 2.5 is absolutely intentional, don't change it.
        },
        "initial_agents": INITIAL_AGENTS,
        "environment": {
            "id": "environment",
            "initial_reality": "A sprawling shantytown built on the interconnected rooftops of a sleeping city.",
        },
    }

    return config
