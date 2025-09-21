# Project: Lore Games

## Project Overview

This project is a Python-based framework for creating dynamic, turn-based simulations with AI agents. The core of the simulation is built around three main components:

*   **`Agent`**: Represents an actor in the simulation with a distinct personality and memory.
*   **`Environment`**: Manages the shared reality of the simulation, processes agent actions, and determines outcomes.
*   **`Interaction`**: A base class for all events and states within the simulation, such as `Perspective`, `Intention`, and `Divination`.

The simulation progresses in a loop where agents perceive the environment, form intentions, and act upon them. The environment then resolves these actions and updates the shared reality.

## Building and Running

This is a Python project. To run the simulation, execute the main script from the root of the project:

```bash
python -m src.main
```

## Development Conventions

*   **Configuration**: The simulation is configured through `src/config.py`, which controls parameters like the number of turns, agent definitions, and logging settings.
*   **State Logging**: The project includes a sophisticated logging mechanism that dumps the state of the simulation to the `.state_dump/` directory. This feature is toggleable in the config and distinguishes between fleeting states (like `Action` and `Intention`) and continuous states (like `Introspection` and `Divination`).
*   **AI Abstraction**: The AI logic is abstracted into the `AIHandler` class in `src/ai_handler.py`. Currently, it uses a dummy implementation that can be replaced with a more advanced AI model.
*   **Type Hinting**: The codebase makes extensive use of Python's type hints for clarity and maintainability.

## Gemini Notes
- Outlines and lists don't seem to render properly in the CLI. It's better to use the scratchpad for this kind of structured text.