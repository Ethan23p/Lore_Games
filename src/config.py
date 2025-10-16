# config.py

"""
Central configuration for the Lore Games simulation.
"""
import os
from typing import Dict, Any, List

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
        "environment": {
            "id": "environment",
            "primer_style": "narrative_writer", # "narrative_writer" or "simulation_engine"
        }
        ,
    }

    return config
