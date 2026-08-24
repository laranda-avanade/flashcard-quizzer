"""
Flashcard data model for the Flashcard Quizzer application.
"""

from dataclasses import dataclass


@dataclass
class Flashcard:
    """Represents a single flashcard with a front (question) and back (answer).
    """

    front: str
    back: str

    def __post_init__(self) -> None:
        """Validate that front and back are non-empty strings."""
        if not isinstance(self.front, str) or not self.front.strip():
            raise ValueError("Flashcard 'front' must be a non-empty string.")
        if not isinstance(self.back, str) or not self.back.strip():
            raise ValueError("Flashcard 'back' must be a non-empty string.")
