# chronicle.py

import os
from functools import singledispatchmethod
from dataclasses import fields
from typing import Coroutine, TypeVar, Any, Dict
from lore_types import (
    BaseAIInteraction, InitialPerspective, Perspective, Intention, Divination, Reality
)
from ai_handler import AIGenerationError

T = TypeVar('T', bound=BaseAIInteraction)

class Chronicle:
    """Handles the logging of simulation state to disk and console."""

    def __init__(self, config: Dict[str, Any], base_path: str = "state_dump"):
        self.base_path = base_path
        self.should_write_file = config.get("write_to_file", False)
        self.should_print_cmd = config.get("print_to_cmd", False)
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
        return f"================== {text} =================="

    # --- Simulation Event Logging ---

    def log_setup_start(self):
        if self.should_print_cmd:
            print(self._create_banner("INITIALIZING SIMULATION"))

    def log_setup_end(self):
        if self.should_print_cmd:
            print("-----------------------------")

    def log_agent_creation(self, agent_name: str):
        if self.should_print_cmd:
            print(f"Created agent: {agent_name}")

    def log_environment_creation(self, env_id: str):
        if self.should_print_cmd:
            print(f"Created environment: {env_id}")

    def log_priming_start(self):
        if self.should_print_cmd:
            print(self._create_banner("PRIMING AGENTS (TURN 0)"))

    def log_priming_end(self):
        if self.should_print_cmd:
            print("---------------------------------")

    def log_turn_start(self, turn_number: int, reality: str):
        if self.should_print_cmd:
            print(self._create_banner(f"TURN {turn_number}"))
            print(f'Reality: "{reality[:80].strip()}..."')

    def log_turn_end(self):
        if self.should_print_cmd:
            print("--- End of Turn ---")

    # --- Console Formatting ---

    @singledispatchmethod
    def _format_for_console(self, interaction: object) -> str | None:
        """Returns a single-line, truncated string for console output."""
        return None # Default to no console output

    @_format_for_console.register
    def _(self, interaction: InitialPerspective) -> str:
        return f"\nPrimed {interaction.owner}."

    @_format_for_console.register
    def _(self, interaction: Perspective) -> str:
        content_str = interaction.content or ""
        return f'\n{interaction.owner} perceives: "{content_str[:80].strip()}..."'

    @_format_for_console.register
    def _(self, interaction: Intention) -> str:
        content_str = interaction.content or ""
        return f'\n{interaction.owner} intends: "{content_str[:80].strip()}..."'

    @_format_for_console.register
    def _(self, interaction: Reality) -> str:
        content_str = interaction.content or ""
        return f'\nNew Reality: "{content_str[:80].strip()}..."'

    # --- File Formatting ---

    def _format_for_file(self, interaction: BaseAIInteraction, filename: str, title: str):
        """A standardized formatter for creating full markdown file content."""
        # Header
        owner_part = f" | Owner: {interaction.owner}" if hasattr(interaction, 'owner') else ""
        header = f"### Turn: {interaction.turn_origin} | {title}{owner_part}\n"

        # Content section is always present
        content_section = f"#### Content\n{interaction.content or 'None'}\n\n"

        # Prompt section is conditional
        prompt_section = ""
        if hasattr(interaction, 'prompt') and interaction.prompt:
            prompt_section = f"#### Prompt\n```\n{interaction.prompt}\n```\n\n"

        # Metadata for all other fields
        metadata_section = "#### Metadata\n"
        has_metadata = False
        for f in fields(interaction):
            excluded_fields = {'prompt', 'content', 'owner', 'turn_origin', 'template_key'}
            if f.name not in excluded_fields:
                value = getattr(interaction, f.name)
                if value:
                    has_metadata = True
                    metadata_section += f"- **{f.name}**: {value}\n"
        
        if has_metadata:
            metadata_section += "\n"

        return (
            header + prompt_section + content_section + (metadata_section if has_metadata else "")
        )

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
        self._process_log(
            interaction,
            filename="reality.md",
            title="Final Reality"
        )