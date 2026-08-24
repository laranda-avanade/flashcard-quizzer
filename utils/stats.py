"""
Session statistics for the Flashcard Quizzer application.

Tracks correct, incorrect, and skipped answers for a quiz session
and provides a score percentage calculation.
"""


class SessionStats:
    """Track and report statistics for a single quiz session.

    Attributes are updated via record_correct, record_incorrect, and
    record_skipped. All counts start at zero and only accept non-negative
    integer increments.
    """

    def __init__(self) -> None:
        self._correct: int = 0
        self._incorrect: int = 0
        self._skipped: int = 0

    @property
    def correct(self) -> int:
        """Number of correctly answered cards."""
        return self._correct

    @property
    def incorrect(self) -> int:
        """Number of incorrectly answered cards."""
        return self._incorrect

    @property
    def skipped(self) -> int:
        """Number of skipped cards."""
        return self._skipped

    @property
    def total_attempted(self) -> int:
        """Total number of cards attempted (correct + incorrect)."""
        return self._correct + self._incorrect

    @property
    def total(self) -> int:
        """Total cards presented including skipped."""
        return self._correct + self._incorrect + self._skipped

    @property
    def score_percentage(self) -> float:
        """Percentage of attempted answers that were correct.

        Returns 0.0 when no answers have been attempted to avoid
        division by zero.

        Returns:
            A float in the range [0.0, 100.0].
        """
        if self.total_attempted == 0:
            return 0.0
        return (self._correct / self.total_attempted) * 100.0

    def record_correct(self, count: int = 1) -> None:
        """Record one or more correct answers.

        Args:
            count: Number of correct answers to record (must be >= 1).

        Raises:
            ValueError: If count is less than 1.
        """
        if count < 1:
            raise ValueError(
                f"count must be at least 1, got {count}."
            )
        self._correct += count

    def record_incorrect(self, count: int = 1) -> None:
        """Record one or more incorrect answers.

        Args:
            count: Number of incorrect answers to record (must be >= 1).

        Raises:
            ValueError: If count is less than 1.
        """
        if count < 1:
            raise ValueError(
                f"count must be at least 1, got {count}."
            )
        self._incorrect += count

    def record_skipped(self, count: int = 1) -> None:
        """Record one or more skipped cards.

        Args:
            count: Number of skipped cards to record (must be >= 1).

        Raises:
            ValueError: If count is less than 1.
        """
        if count < 1:
            raise ValueError(
                f"count must be at least 1, got {count}."
            )
        self._skipped += count

    def reset(self) -> None:
        """Reset all counters to zero."""
        self._correct = 0
        self._incorrect = 0
        self._skipped = 0

    def summary(self) -> str:
        """Return a plain-text summary of the session statistics.

        Returns:
            A formatted string with counts and score percentage.
        """
        return (
            f"Correct: {self._correct} | "
            f"Incorrect: {self._incorrect} | "
            f"Skipped: {self._skipped} | "
            f"Score: {self.score_percentage:.1f}%"
        )
