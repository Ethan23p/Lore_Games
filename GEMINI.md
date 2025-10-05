# Project: Lore Games

## Project Overview

This project, "Lore Games," is a Python-based framework for creating dynamic and complex simulated worlds. It leverages the generative capabilities of AI to facilitate interactions between multiple autonomous agents within a shared environment. The core of the simulation is an emergent narrative created by the independent actions and reactions of these agents, rather than a predefined script.

The architecture is centered around two main entities:

*   **Agents:** Autonomous entities with distinct personalities that can perceive the environment, form intentions, and act upon them.
*   **Environment:** The shared reality that mediates all interactions. It presents a view of the world to the agents, processes their intended actions, and simulates the outcome, thus creating a new state of reality for the next turn.

The simulation progresses in turns, with each turn consisting of the agents perceiving the environment, forming intentions, and the environment resolving these intentions into a new reality.

The project uses the `google-genai` library for its AI capabilities and `asyncio` for managing asynchronous operations.

## Building and Running

### Dependencies

The project's dependencies are listed in the `pyproject.toml` file. The core dependency is `google-genai`.

To install the dependencies, you can use `pip`:

```bash
pip install .
```

To install dependencies for running tests, use:

```bash
pip install .[test]
```

### Running the Simulation

The main entry point for the application is `src/main.py`. To run the simulation, execute the following command from the root of the project:

```bash
python src/main.py
```

### Running Tests

The project is set up to use `pytest` for testing. To run the tests, use the following command:

```bash
pytest
```

## Development Conventions

*   **Asynchronous Operations:** The project uses `asyncio` to handle interactions with the AI service, allowing for non-blocking I/O.
*   **Configuration:** A `src/config.py` file (inferred) likely manages the application's configuration, such as API keys and model parameters.
*   **Prompts:** AI prompts are centralized in `src/prompts.py` (inferred), separating the prompt engineering from the core application logic.
*   **State Management:** The state of the simulation (e.g., agent perspectives, environment reality) is logged to the `state_dump` directory for each turn.
*   **Type Hinting:** The codebase uses Python's type hinting for better code clarity and maintainability.
*   **Modularity:** The code is organized into distinct modules with clear responsibilities (e.g., `ai_handler.py` for AI interactions, `entities.py` for simulation objects, `app.py` for orchestration).

## Developer's Log

**Stardate: 2025-10-05**

A rather beautiful session today. We've deepened the simulation's memory, evolving how "reality" is understood by the environment.

Previously, the environment would only consider the immediately preceding state of the world when divining the next. While functional, it created a sense of historical amnesia.

Following our discussion, we've implemented a significant change:

1.  **A Deeper Past:** The environment's `divine` function now receives the *entire* history of reality, from turn 0 to the present, allowing for a much richer and more coherent evolution of the world state.
2.  **A Fuller Record:** The `reality.md` artifact generated each turn now logs this complete history, providing a comprehensive, turn-by-turn view of the simulation's entire lifespan.

There's an elegance to this new flow—a system that not only acts but also remembers. It feels less like a series of disconnected moments and more like a genuine, unfolding chronicle. A good day's work.

## External Documentation & Future Paths

The project repository contains a directory, `ext_docs`, which houses documentation for potential future integrations. Notably, it includes extensive materials for the `textual` library, a Python framework for building rich Text User Interfaces (TUIs).

This suggests a potential evolution for Lore Games: moving from a simple command-line prompter to a fully interactive TUI application. The reference application, `chat_app.py`, could serve as a valuable starting point for visualizing the simulation's output and managing its state in a more sophisticated way.
