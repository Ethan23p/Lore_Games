# chronicle.py

import os
from functools import singledispatchmethod
from dataclasses import fields, is_dataclass
from lore_types import (
    BaseAIInteraction, InitialPerspective, Perspective, Intention, Divination, Reality
)

class Chronicle:
    """Handles the logging of simulation state to disk."""

    def __init__(self, base_path: str = "state_dump"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _write_file(self, turn: int, filename: str, content: str):
        """Helper to write content to a turn-specific directory."""
        turn_dir = os.path.join(self.base_path, f"turn_{turn:03d}")
        os.makedirs(turn_dir, exist_ok=True)
        with open(os.path.join(turn_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)

    @singledispatchmethod
    def log(self, interaction: object, **kwargs):
        """Generic logger for unknown types."""
        print(f"Warning: No specific chronicle logger for type {type(interaction)}")

    @log.register
    def _(self, interaction: InitialPerspective):
        filename = f"{interaction.owner}_initial_perspective.md"
        self._log_standard_interaction(interaction, filename)

    @log.register
    def _(self, interaction: Perspective):
        filename = f"{interaction.owner}_perspective.md"
        self._log_standard_interaction(interaction, filename)

    @log.register
    def _(self, interaction: Intention):
        filename = f"{interaction.owner}_intention.md"
        self._log_standard_interaction(interaction, filename)

    @log.register
    def _(self, interaction: Divination):
        filename = f"{interaction.owner}_divination.md"
        self._log_standard_interaction(interaction, filename)

    @log.register
    def _(self, interaction: Reality):
        filename = "reality.md"
        header = f"### Turn: {interaction.turn_origin} | Final Reality\n\n"
        self._write_file(interaction.turn_origin, filename, header + interaction.content)

    def _log_standard_interaction(self, interaction: BaseAIInteraction, filename: str):
        """A standardized formatter for most interaction types."""
        # Header
        header = f"### Turn: {interaction.turn_origin} | Owner: {interaction.owner}\n"

        # Prioritize prompt and content
        prompt_section = f"#### Prompt\n```\n{interaction.prompt}\n```\n\n" if interaction.prompt else ""
        content_section = f"#### Content\n{interaction.content}\n\n"

        # Metadata for all other fields
        metadata_section = "#### Metadata\n```\n"
        for f in fields(interaction):
            if f.name not in ['prompt', 'content', 'owner', 'turn_origin', 'template_key']:
                value = getattr(interaction, f.name)
                metadata_section += f"{f.name}: {value}\n"
        metadata_section += "```\n"

        full_content = (
            header + prompt_section + content_section + metadata_section
        )
        self._write_file(interaction.turn_origin, filename, full_content)