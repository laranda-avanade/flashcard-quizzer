"""
File handling utility for data persistence and flashcard loading.

This module demonstrates file I/O operations and error handling
patterns that students can learn from and extend.
"""

import json
from typing import Any, Dict, List
from pathlib import Path

from utils.flashcard import Flashcard


class FileHandler:
    """Handle file operations for data persistence."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_data(self, filename: str, data: Dict[str, Any]) -> None:
        """Save data to a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
        except (IOError, TypeError) as e:
            raise RuntimeError(f"Failed to save data to {filename}: {e}")

    def load_data(self, filename: str) -> Dict[str, Any]:
        """Load data from a JSON file."""
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load data from {filename}: {e}")

    def file_exists(self, filename: str) -> bool:
        """Check if a file exists in the data directory."""
        return (self.data_dir / filename).exists()

    def delete_file(self, filename: str) -> None:
        """Delete a file from the data directory."""
        filepath = self.data_dir / filename
        if filepath.exists():
            filepath.unlink()

    def list_files(self) -> List[str]:
        """List all files in the data directory."""
        return [f.name for f in self.data_dir.iterdir() if f.is_file()]

    @staticmethod
    def load_flashcards(filepath: str) -> List[Flashcard]:
        """Load and validate flashcards from a JSON file at an arbitrary path.

        Supports two JSON formats:
          - Flat list:   [{"front": "...", "back": "..."}, ...]
          - Wrapped:     {"cards": [{"front": "...", "back": "..."}, ...]}

        Args:
            filepath: Absolute or relative path to the JSON file.

        Returns:
            A list of validated Flashcard objects.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the JSON is malformed, has an unexpected structure,
                        contains no cards, or any card fails validation.
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(
                f"Flashcard file not found: '{filepath}'"
            )

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Malformed JSON in '{filepath}': {exc}"
            ) from exc

        if isinstance(raw, list):
            cards_data = raw
        elif isinstance(raw, dict) and "cards" in raw:
            cards_data = raw["cards"]
        else:
            raise ValueError(
                f"'{filepath}' must be a JSON array or an object with a "
                f"'cards' key, got {type(raw).__name__}."
            )

        if not isinstance(cards_data, list):
            raise ValueError(
                f"'cards' in '{filepath}' must be a list, "
                f"got {type(cards_data).__name__}."
            )

        if not cards_data:
            raise ValueError(f"No flashcards found in '{filepath}'.")

        flashcards: List[Flashcard] = []
        for index, item in enumerate(cards_data):
            if not isinstance(item, dict):
                raise ValueError(
                    f"Card at index {index} must be an object, "
                    f"got {type(item).__name__}."
                )
            if "front" not in item:
                raise ValueError(
                    f"Card at index {index} is missing the 'front' key."
                )
            if "back" not in item:
                raise ValueError(
                    f"Card at index {index} is missing the 'back' key."
                )
            try:
                flashcards.append(
                    Flashcard(front=item["front"], back=item["back"])
                )
            except ValueError as exc:
                raise ValueError(
                    f"Card at index {index} is invalid: {exc}"
                ) from exc

        return flashcards
