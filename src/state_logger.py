# src/state_logger.py
import os
import shutil
from pathlib import Path

class StateLogger:
    """
    Handles writing simulation state and AI prompts to disk for debugging.
    """
    def __init__(self, output_dir: str = ".state_dump"):
        """
        Initializes the logger and ensures the output directory exists.

        Args:
            output_dir: The directory where log files will be saved.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def clear_turn_logs(self):
        """
        Clears the log directory to ensure only the most recent turn's
        data is present.
        """
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def log_prompt(self, filename: str, content: str):
        """
        Logs a given string content to a file in the output directory.

        Args:
            filename: The name of the file to write to.
            content: The string content to write to the file.
        """
        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
