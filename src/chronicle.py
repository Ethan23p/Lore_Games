# chronicle.py

import os
import textwrap
from functools import singledispatchmethod
from dataclasses import fields
from typing import Coroutine, TypeVar, Any, Dict

from .lore_types import (
    BaseAIInteraction, InitialPerspective, Perspective, Intention, Divination, Reality
)
from .ai_handler import AIGenerationError

T = TypeVar('T', bound=BaseAIInteraction)

class Chronicle:
    """Handles the logging of simulation state to disk and console."""

    def __init__(self, config: Dict[str, Any], base_path: str = "state_dump"):
        self.base_path = base_path
        self.should_write_file = config.get("write_to_file", False)
        self.should_print_cmd = config.get("print_to_cmd", False)
        self.debug_mode = config.get("debug_mode", False)
        if self.should_write_file:
            os.makedirs(self.base_path, exist_ok=True)

    async def execute_and_log(self, interaction_coro: Coroutine[Any, Any, T]) -> T:
        """Awaits an interaction coroutine, logs it, and returns the result."""
        try:
            result = await interaction_coro
            self.log(result)
            return result
        except AIGenerationError as e:
            print(f"FATAL: An AI generation error occurred: {e}")
            raise

    def _create_banner(self, text: str) -> str:
        """Creates a single-line banner for console output."""
        return f"\n================== {text} =================="

    # --- Simulation Event Logging ---

    def log_setup_start(self):
        if self.should_print_cmd:
            print(self._create_banner("INITIALIZING SIMULATION"))

    def log_setup_end(self):
        if self.should_print_cmd:
            print("\n-----------------------------")

    def log_agent_creation(self, agent_name: str):
        if self.should_print_cmd:
            print(f"\nCreated agent: {agent_name}")

    def log_environment_creation(self, env_id: str):
        if self.should_print_cmd:
            print(f"\nCreated environment: {env_id}")

    def log_priming_start(self):
        if self.should_print_cmd:
            print(self._create_banner("\nPRIMING AGENTS (TURN 0)\n"))

    def log_priming_end(self):
        if self.should_print_cmd:
            print("\n---------------------------------\n")

    def log_turn_start(self, turn_number: int, reality: str):
        if self.should_print_cmd:
            print(self._create_banner(f"TURN {turn_number}"))
            print(f'\nReality: "{reality[:80].strip()}..."\n')

    def log_turn_end(self):
        if self.should_print_cmd:
            print("\n--- End of Turn ---\n")

    # --- Console Formatting ---

    @singledispatchmethod
    def _format_for_console(self, interaction: object) -> str | None:
        """Returns a single-line, truncated string for console output."""
        return None # Default to no console output

    @_format_for_console.register
    def _(self, interaction: InitialPerspective) -> str:
        return f"\nPrimed {interaction.owner}.\n"

    @_format_for_console.register
    def _(self, interaction: Perspective) -> str:
        content_str = interaction.content or ""
        return f'\n{interaction.owner} perceives: "\n{content_str[:80].strip()}..."\n'

    @_format_for_console.register
    def _(self, interaction: Intention) -> str:
        content_str = interaction.content or ""
        return f'\n{interaction.owner} intends: "\n{content_str[:80].strip()}..."\n'

    @_format_for_console.register
    def _(self, interaction: Reality) -> str:
        content_str = interaction.content or ""
        return f'\nNew Reality: "\n{content_str[:80].strip()}..."\n'

    # --- File Formatting ---

    def _format_for_file(self, interaction: BaseAIInteraction, filename: str, title: str):
        """A standardized formatter for creating full markdown file content."""
        # Header
        owner_part = f" | Owner: {interaction.owner}" if hasattr(interaction, 'owner') else ""
        header = f"### Turn: {interaction.turn_origin} | {title}{owner_part}\n\n"

        # Content section is always present
        display_content = interaction.content or 'None'
        content_section = f"\n#### Content\n\n{display_content}\n\n"

        # Prompt section is now always included if available
        prompt_section = ""
        if hasattr(interaction, 'prompt') and interaction.prompt:
            dedented_prompt = textwrap.dedent(interaction.prompt).strip()
            prompt_section = f"\n#### Prompt\n\n{dedented_prompt}\n\n"

        # Metadata section is conditional on debug_mode
        metadata_section = ""
        if self.debug_mode:
            metadata_fields = []
            for f in fields(interaction):
                excluded_fields = {'prompt', 'content', 'owner', 'turn_origin', 'template_key', 'full_history'}
                if f.name not in excluded_fields:
                    value = getattr(interaction, f.name)
                    if value:
                        metadata_fields.append(f"\n- **{f.name}**:\n{value}\n\n")

            if metadata_fields:
                metadata_section = "\n#### Metadata\n\n" + "".join(metadata_fields)

        return header + content_section + prompt_section + metadata_section

    # --- Main Logger ---

    @singledispatchmethod
    def log(self, interaction: object):
        """Generic logger for unknown types."""
        print(f"Warning: No specific chronicle logger for type {type(interaction)}")

    def _process_log(self, interaction, filename: str, title: str):
        """Central handler for console and file output."""
        if self.should_print_cmd:
            console_output = self._format_for_console(interaction)
            if console_output:
                print(console_output)
        if self.should_write_file:
            file_content = self._format_for_file(interaction, filename, title)
            turn_dir = os.path.join(self.base_path, f"turn_{interaction.turn_origin:03d}")
            os.makedirs(turn_dir, exist_ok=True)
            with open(os.path.join(turn_dir, filename), 'w', encoding='utf-8') as f:
                f.write(file_content)

    @log.register
    def _(self, interaction: InitialPerspective):
        self._process_log(
            interaction,
            filename=f"{interaction.owner}_initial_perspective.md",
            title="Initial Perspective"
        )

    @log.register
    def _(self, interaction: Perspective):
        self._process_log(
            interaction,
            filename=f"{interaction.owner}_perspective.md",
            title="Perspective"
        )

    @log.register
    def _(self, interaction: Intention):
        self._process_log(
            interaction,
            filename=f"{interaction.owner}_intention.md",
            title="Intention"
        )

    @log.register
    def _(self, interaction: Divination):
        # Divination is internal, so we only write it to a file if specified.
        if self.should_write_file:
            self._process_log(
                interaction,
                filename=f"{interaction.owner}_divination.md",
                title="Divination"
            )

    @log.register
    def _(self, interaction: Reality):
        """Specialized logger for the final Reality object."""
        if self.should_print_cmd:
            console_output = self._format_for_console(interaction)
            if console_output:
                print(console_output)

        if self.should_write_file:
            title = "Final Reality"
            owner_part = f" | Owner: {interaction.owner}"
            header = f"### Turn: {interaction.turn_origin} | {title}{owner_part}\n\n"
            content_section = f"\n#### Content\n\n{interaction.content}\n\n"
            history_section = f"\n#### Full History\n\n{interaction.full_history}\n\n"

            file_content = header + content_section + history_section
            turn_dir = os.path.join(self.base_path, f"turn_{interaction.turn_origin:03d}")
            os.makedirs(turn_dir, exist_ok=True)
            with open(os.path.join(turn_dir, "reality.md"), 'w', encoding='utf-8') as f:
                f.write(file_content)