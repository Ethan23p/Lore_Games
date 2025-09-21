## Simple flow

	init()
		env.init()
		for each: agent
			agent.init()
			env.reflect(agent name)
	simple_loop()
		for each: agent
			agent.planning()
				prompt = prompt_library.simple_flow.planning
				plan = agent.generate(prompt)
				env.gather_plans(agent name, plan)
		env.divine(agents' plans)

### Flow-Aware Prompt System Plan (2025-09-12)

Here is the plan to refactor the system so that each interaction uses the correct prompt for the currently active flow.

1.  **Make `Interaction` Subclasses Flow-Aware:**
    *   **Problem:** Currently, `Interaction` subclasses like `Divination` and `Perspective` have the flow name hardcoded (e.g., `PromptLibrary.TEMPLATES["main_flow"]["divination"]`).
    *   **Solution:** I will modify the `__init__` method of all relevant `Interaction` subclasses (`Divination`, `Intention`, `Introspection`, `Action`, `Plan`, `Perspective`) in `src/lore_objects.py`. The hardcoded string `"main_flow"` or `"simple_flow"` will be replaced with a dynamic f-string: `f"{config.FLOW}_flow"`. This will ensure that when an interaction is created, it automatically selects the correct prompt template from the `PromptLibrary` based on the global `FLOW` setting in `src/config.py`.

### Primer & Prompt Refactor To-Do (2025-09-12)

Based on your latest notes, here is the revised plan:

1.  **Implement Flow-Aware Prompts with Fallback:**
    *   **Goal:** Make `Interaction` objects automatically use the prompt for the current flow (`simple_flow` or `main_flow`), but default to the `main_flow` version if a flow-specific one doesn't exist.
    *   **Action:**
        *   In `src/lore_objects.py`, I will create a new private helper function, `_get_prompt_template(interaction_type: str)`.
        *   This function will first try to find a prompt in `PromptLibrary.TEMPLATES` using the current flow from `config.FLOW`.
        *   If it encounters a `KeyError` (meaning the prompt doesn't exist for the current flow), it will catch the error and instead return the prompt from the `"main_flow"`.
        *   I will then update the `__init__` method of every `Interaction` subclass (`Perspective`, `Introspection`, `Intention`, `Action`, `Divination`, `Plan`) to use this new helper function instead of a hardcoded path.

2.  **Implement Primer Injection:**
    *   **Goal:** Ensure that every prompt sent to the AI is prepended with the correct "primer" (`agent` or `environment`) to give the AI its core instructions for that interaction.
    *   **Action:**
        *   I will modify the `Interaction.generate` method signature in `src/lore_objects.py` to accept a new `primer: str` argument.
        *   Inside `generate`, I will prepend this `primer` to the specific prompt (from `_create_prompt`) before sending the final, combined text to the `AIHandler`. The full prompt will be saved for logging.
        *   I will then trace all calls to `.generate()` within the `Agent` and `Environment` classes and update them to pass their respective `self.primer` string.