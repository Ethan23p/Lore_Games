
# TUI Implementation Plan: From Prototype to Full Integration

This document outlines the iterative steps to develop a Textual-based user interface for the Lore Games simulation. We will evolve the TUI from a simple, static view into a fully interactive dashboard.

---

## Phase 1: Foundational Setup (The "Is It Plugged In?" Test)

**Goal:** Create the most basic TUI possible. This phase validates that a Textual app can be launched, can read a file from our project, and can register a button press.

**Steps:**

1.  **Create `src/tui.py`:** This file will house our main TUI application class, `LoreGamesApp`.
2.  **Basic App Structure:** Borrowing from `ext_docs/textual_reference_app/chat_app.py`, create an `App` class with a `compose` method.
3.  **Minimalist Layout:** The `compose` method will create a simple layout:
    *   A `Header` and `Footer`.
    *   A `RichLog` widget that will serve as our main content display.
    *   A `Button` with the label "Next Turn".
4.  **Display Static Data:** In the `on_mount()` method, read the contents of `src/config.py` and write them into the `RichLog`. This confirms the TUI can access project files.
5.  **Placeholder Action:** Create an event handler for the "Next Turn" button using the `@on(Button.Pressed)` decorator. When clicked, it will simply write a message like `"ACTION: Advance to next turn."` into the `RichLog`.
6.  **New Entry Point:** Modify `src/main.py` to import and run `LoreGamesApp` from `tui.py`. This makes the TUI the new front door to our application.

---

## Phase 2: Connecting the Simulation Engine

**Goal:** Wire up the "Next Turn" button to actually drive the simulation. The TUI will become a true controller for the simulation's progression.

**Steps:**

1.  **Refactor Core Logic:** Modify `src/app.py` to make the simulation controllable. The existing main loop will be split into two distinct methods:
    *   `initialize_simulation()`: Sets up the world, agents, and turn 0 state.
    *   `run_single_turn()`: Executes one complete turn cycle (perception, intention, divination).
2.  **Integrate Simulation Instance:** In `src/tui.py`, import the simulation app. The `LoreGamesApp` will create and hold an instance of the simulation engine (e.g., `self.simulation = SimulationApp()`).
3.  **Initialize on Start:** The TUI's `on_mount()` method will now call `self.simulation.initialize_simulation()`.
4.  **Activate the "Next Turn" Button:** The button's event handler will be updated to call `self.simulation.run_single_turn()`.
5.  **Log Turn Completion:** After the simulation turn is complete, the handler will write a confirmation to the `RichLog`, like `f"Turn {self.simulation.turn_number} complete."`.

---

## Phase 3: Visualizing the World State

**Goal:** Make the TUI display the dynamic state of the simulation. This involves activating the sidebar and using it to select different views of the world.

**Steps:**

1.  **Implement the Navigator:** Add a `ListView` to the left side of the layout. Populate it with the primary views: `["Timeline", "Environment", "Charlie", "Delta"]`.
2.  **Handle View Selection:** Implement the `on_list_view_selected` event handler. This will fire when the user clicks an item in the Navigator.
3.  **Fetch and Display State:** Inside the handler, based on the selected view, the app will:
    a. Identify the current turn number.
    b. Read the content from the corresponding file in the `state_dump` directory (e.g., `turn_00X/reality.md` for the "Environment" view).
    c. Clear the `RichLog` and write the new content to it.
4.  **Automatic Refresh:** After the "Next Turn" button is pressed and the simulation completes, the TUI will automatically refresh the main content area with the new data for the currently selected view.

---

## Phase 4: Polish and Advanced Features

**Goal:** Improve the user experience and make the application more robust and informative.

**Steps:**

1.  **Asynchronous Turns & Loading Indicator:** Refactor the `run_single_turn()` call to be asynchronous using a Textual `@work` decorator. While the simulation is processing, display a `LoadingIndicator` and temporarily disable the "Next Turn" button.
2.  **Dynamic Footer:** Use the `Footer` to display the current turn number and simulation status (e.g., "Awaiting user input", "Processing turn...").
3.  **Error Handling:** Wrap the call to the simulation engine in a try/except block. If the simulation raises an error, display it cleanly in the `RichLog` instead of crashing the TUI.
4.  **Future-Proofing:** Re-introduce the `Input` widget from the reference app, but keep it disabled for now. This reserves a space for future interactive commands.
