"""
Central configuration for the Lore Games simulation.
"""

# Simulation parameters
LOGGING_ENABLED = True
NUM_TURNS = 3

# Agent configuration
AGENTS = [
    {
        "name": "Charlie",
        "personality": "A cautious and observant individual.",
    },
    {
        "name": "Delta",
        "personality": "An aggressive and impulsive individual.",
    },
]

# Environment configuration
INITIAL_REALITY = "A vast, empty plain under a grey sky."