"""
Central configuration for the Lore Games simulation.
"""

# Simulation parameters
LOGGING_ENABLED = True
DEBUG_PRINTING_ENABLED = True
FLOW = "simple"  # Can be "main" or "simple"
MAX_TOKENS = 1536

# Agent configuration
AGENTS = [
    {
        "name": "Charlie",
        "personality": "A goblin which survived being thrown into a ceremonial bonfire; Delta has a new appreciation for life.",
    },
    {
        "name": "Delta",
        "personality": "A mechanoid which speaks through a lo-fi speaker, Charlie is fascinated by biology.",
    },
]

# Environment configuration
INITIAL_REALITY = "A sprawling shantytown built on the interconnected rooftops of a sleeping city."