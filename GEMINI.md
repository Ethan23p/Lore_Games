# Project: Lore Games

## Project Overview

This project is a sophisticated, turn-based simulation engine designed to model interactions between AI-driven agents within a dynamic environment. The core of the project is a rich, object-oriented domain model that defines the taxonomy of interactions (Perception, Introspection, Action) and entities (Agents, Environment).

The system is architected around a "tell, don't ask" philosophy, where the environment mediates all reality and tells agents what they perceive. Agents, in turn, process this information internally and tell the environment their intended actions. The entire simulation is designed to be driven by generative AI, with the Python code serving as the "pipes" to connect various AI contexts.

The project is currently in a mock-up phase, with a clear separation between the simulation logic (`src/lore_types.py`), the AI prompt handling (`src/ai_handler.py`), the application entry point (`src/main.py`), and state logging (`src/state_logger.py`). The ultimate goal is to integrate this simulation engine with the `fast-agent-mcp` framework to create a fully-fledged AI agent application.

**Key Technologies:**
*   **Language:** Python (>=3.13)
*   **Framework:** `fast-agent-mcp`
*   **Testing:** `pytest`
*   **Core Architecture:** Object-Oriented Programming, Type Hinting

## Core Architecture

The simulation is composed of several key classes:

*   **`Agent`**: Represents an autonomous entity that can perceive, think, and act. Each agent has a personality that influences its AI-generated responses.
*   **`Environment`**: Manages the state of the world and orchestrates the simulation turns. It provides agents with perceptions and processes their intended actions.
*   **`AIHandler`**: A centralized module responsible for all interactions with the (mock) AI. It formats prompts based on the simulation's context and returns AI-generated content.
*   **`StateLogger`**: A utility class that logs the prompts sent to the `AIHandler` to disk. This is useful for debugging and understanding the AI's decision-making process.

## Building and Running

The project uses `uv` for environment and dependency management, as indicated by the `uv.lock` file.

### Dependencies

To install the required dependencies, including the optional testing packages, run:

```bash
uv pip install -e .[test]
```

### Running the Simulation Mock-up

The current entry point runs a mock simulation that prints the logical flow of a few turns to the console. To run it, execute the main module from the project's root directory:

```bash
uv run -m src.main
```

### Running Tests

The project uses `pytest` for testing. To run the test suite, execute the following command from the project's root directory:

```bash
uv run -m pytest
```

## Development Conventions

*   **Strong Typing:** The codebase heavily utilizes Python's `typing` module. New types are created with `NewType` for clarity and type safety (e.g., `AgentId`, `TurnId`). All new code should be fully type-hinted.
*   **Object-Oriented Design:** The simulation is built on a clear class hierarchy (`Entity`, `Interaction`). New logic should be encapsulated within the appropriate class methods. The main simulation loop is encapsulated in the `Environment.run_turn` method.
*   **Testing:** Tests are located in the `tests/` directory. New features should be accompanied by unit tests that verify their functionality. The current tests serve as "smoke tests" to ensure class initialization is working correctly.
*   **Configuration:** The main simulation runner in `src/main.py` uses a simple dictionary as a configuration stub. This pattern should be maintained for setting up initial simulation parameters.
*   **State Logging:** The `StateLogger` class provides a mechanism for inspecting the prompts sent to the AI. When enabled, it writes the prompts to the `.state_dump/` directory, which is useful for debugging and understanding the simulation's flow.