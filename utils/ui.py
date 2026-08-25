"""
Interactive UI layer for the Flashcard Quizzer application.

Provides QuizSession, which coordinates a QuizMode, SessionStats,
and terminal I/O for an interactive quiz session.
"""

from typing import Callable, List, Optional

import colorama
from colorama import Fore, Style

from utils.flashcard import Flashcard
from utils.quiz_engine import QuizMode
from utils.stats import SessionStats

colorama.init(autoreset=True)

_SKIP_COMMAND = "skip"
_EXIT_COMMAND = "exit"


def _green(text: str) -> str:
    """Return text wrapped in green ANSI codes."""
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def _red(text: str) -> str:
    """Return text wrapped in red ANSI codes."""
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


class QuizSession:
    """Coordinate a quiz session: present cards, collect answers, track stats.

    Dependency injection is used for input and output callables so that the
    session logic can be exercised in tests without terminal interaction.

    Args:
        mode: An initialised QuizMode strategy (already started with cards).
        stats: A SessionStats instance to record results into.
        input_fn: Callable used to read user input (default: built-in input).
        print_fn: Callable used to display output (default: built-in print).
    """

    def __init__(
        self,
        mode: QuizMode,
        stats: SessionStats,
        input_fn: Optional[Callable[[str], str]] = None,
        print_fn: Optional[Callable[..., None]] = None,
    ) -> None:
        self._mode = mode
        self._stats = stats
        self._input = input_fn if input_fn is not None else input
        self._print = print_fn if print_fn is not None else print

    @property
    def stats(self) -> SessionStats:
        """The SessionStats instance for this session."""
        return self._stats

    def _check_answer(self, user_answer: str, correct_answer: str) -> bool:
        """Compare user_answer and correct_answer case-insensitively.

        Leading and trailing whitespace is stripped before comparison.

        Args:
            user_answer: The string the user typed.
            correct_answer: The expected answer from the Flashcard.

        Returns:
            True if the answers match, False otherwise.
        """
        return user_answer.strip().lower() == correct_answer.strip().lower()

    def _prompt_answer(self, card: Flashcard) -> str:
        """Display the card front and collect a user response.

        Args:
            card: The flashcard to display.

        Returns:
            The raw string entered by the user.
        """
        self._print(f"\nQuestion: {card.front}")
        return self._input("Your answer (or 'skip' / 'exit'): ")

    def _handle_correct(self, card: Flashcard) -> None:
        """Display correct feedback and update stats and mode."""
        self._print(_green("Correct!"))
        self._stats.record_correct()
        self._mode.record_answer(card, correct=True)

    def _handle_incorrect(self, card: Flashcard) -> None:
        """Display incorrect feedback, show the answer, update stats/mode."""
        self._print(_red(f"Incorrect. The correct answer is: {card.back}"))
        self._stats.record_incorrect()
        self._mode.record_answer(card, correct=False)

    def _handle_skip(self, card: Flashcard) -> None:
        """Record a skipped card and notify the mode."""
        self._print("Skipped.")
        self._stats.record_skipped()
        self._mode.record_answer(card, correct=False)

    def run(self, cards: List[Flashcard]) -> SessionStats:
        """Run the interactive quiz session.

        Presents cards according to the quiz mode until all cards are
        exhausted or the user exits. Handles KeyboardInterrupt gracefully.

        Args:
            cards: The list of Flashcard objects to quiz on.

        Returns:
            The SessionStats instance with final session results.
        """
        if not cards:
            self._print("No flashcards to display. Exiting.")
            return self._stats

        self._mode.start(cards)
        self._print(
            "Quiz started. Type 'exit' to quit or 'skip' to skip a card."
        )

        try:
            while not self._mode.is_complete():
                card = self._mode.next_card()
                if card is None:
                    break

                raw = self._prompt_answer(card)
                command = raw.strip().lower()

                if command == _EXIT_COMMAND:
                    self._print("Quiz ended by user.")
                    break

                if command == _SKIP_COMMAND:
                    self._handle_skip(card)
                    continue

                if self._check_answer(raw, card.back):
                    self._handle_correct(card)
                else:
                    self._handle_incorrect(card)

        except (KeyboardInterrupt, EOFError):
            self._print("\nQuiz interrupted. Exiting.")

        self._print(f"\nSession complete. {self._stats.summary()}")
        return self._stats
