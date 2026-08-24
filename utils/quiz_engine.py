"""
Quiz engine for the Flashcard Quizzer application.

Implements the Strategy Pattern for quiz modes and a Factory Pattern
for selecting the appropriate mode at runtime.
"""

import random
from abc import ABC, abstractmethod
from collections import deque
from typing import List, Optional

from utils.flashcard import Flashcard


class QuizMode(ABC):
    """Abstract base class for the quiz mode interface (Strategy Pattern)."""

    @abstractmethod
    def start(self, cards: List[Flashcard]) -> None:
        """Initialise the mode with the full card deck.

        Args:
            cards: The list of flashcards to quiz on.
        """

    @abstractmethod
    def next_card(self) -> Optional[Flashcard]:
        """Return the next card to present, or None when the session ends.

        Returns:
            The next Flashcard, or None if no more cards remain.
        """

    @abstractmethod
    def record_answer(self, card: Flashcard, correct: bool) -> None:
        """Record the result of the user's answer for the current card.

        Args:
            card: The card that was just answered.
            correct: True if the answer was correct, False otherwise.
        """

    @abstractmethod
    def is_complete(self) -> bool:
        """Return True when the session has no more cards to present."""


class SequentialMode(QuizMode):
    """Present every card exactly once in their original order."""

    def __init__(self) -> None:
        self._queue: deque = deque()

    def start(self, cards: List[Flashcard]) -> None:
        """Load cards into the queue in original order."""
        self._queue = deque(cards)

    def next_card(self) -> Optional[Flashcard]:
        """Return the next card or None if the queue is empty."""
        if self._queue:
            return self._queue.popleft()
        return None

    def record_answer(self, card: Flashcard, correct: bool) -> None:
        """No special handling needed for sequential mode."""

    def is_complete(self) -> bool:
        """Return True when all cards have been presented."""
        return len(self._queue) == 0


class RandomMode(QuizMode):
    """Present every card exactly once in a randomly shuffled order."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialise with an optional random seed for deterministic testing.

        Args:
            seed: Optional seed for the random number generator.
        """
        self._seed = seed
        self._queue: deque = deque()

    def start(self, cards: List[Flashcard]) -> None:
        """Shuffle the cards and load them into the queue."""
        shuffled = list(cards)
        rng = random.Random(self._seed)
        rng.shuffle(shuffled)
        self._queue = deque(shuffled)

    def next_card(self) -> Optional[Flashcard]:
        """Return the next shuffled card or None if the queue is empty."""
        if self._queue:
            return self._queue.popleft()
        return None

    def record_answer(self, card: Flashcard, correct: bool) -> None:
        """No special handling needed for random mode."""

    def is_complete(self) -> bool:
        """Return True when all cards have been presented."""
        return len(self._queue) == 0


class AdaptiveMode(QuizMode):
    """Prioritise incorrectly answered cards by placing them in a retry queue.

    Algorithm:
      1. Cards are drawn from the main deck one at a time.
      2. When answered incorrectly the card is appended to the retry queue.
      3. Once the main deck is exhausted, cards are drawn from the retry queue.
      4. A card drawn from the retry queue that is answered correctly is
         removed permanently.
      5. A card drawn from the retry queue that is answered incorrectly is
         appended to the end of the retry queue again (at most once per pass
         to prevent infinite repetition within a single retry round).
      6. The session ends when both the main deck and the retry queue are
         empty, guaranteeing termination.
    """

    def __init__(self) -> None:
        self._deck: deque = deque()
        self._retry: deque = deque()
        self._current_retry_pass_size: int = 0
        self._retry_seen_this_pass: int = 0

    def start(self, cards: List[Flashcard]) -> None:
        """Load cards into the main deck in original order."""
        self._deck = deque(cards)
        self._retry = deque()
        self._current_retry_pass_size = 0
        self._retry_seen_this_pass = 0

    def next_card(self) -> Optional[Flashcard]:
        """Return the next card from the deck or retry queue, or None."""
        if self._deck:
            return self._deck.popleft()

        if self._retry:
            if self._current_retry_pass_size == 0:
                self._current_retry_pass_size = len(self._retry)
                self._retry_seen_this_pass = 0
            if self._retry_seen_this_pass < self._current_retry_pass_size:
                self._retry_seen_this_pass += 1
                card = self._retry.popleft()
                if self._retry_seen_this_pass == self._current_retry_pass_size:
                    self._current_retry_pass_size = 0
                return card

        return None

    def record_answer(self, card: Flashcard, correct: bool) -> None:
        """Place incorrectly answered cards into the retry queue.

        Cards re-enqueued here are always deferred to the next pass;
        the current pass size is never modified after it is set.

        Args:
            card: The card that was just answered.
            correct: True if the answer was correct, False otherwise.
        """
        if not correct:
            self._retry.append(card)

    def is_complete(self) -> bool:
        """Return True when both the deck and retry queue are empty."""
        return len(self._deck) == 0 and len(self._retry) == 0


class QuizModeFactory:
    """Factory for creating QuizMode instances by name (Factory Pattern)."""

    _MODES = {
        "sequential": SequentialMode,
        "random": RandomMode,
        "adaptive": AdaptiveMode,
    }

    @staticmethod
    def create(mode: str) -> QuizMode:
        """Return a QuizMode instance for the given mode name.

        Args:
            mode: One of "sequential", "random", or "adaptive".

        Returns:
            A new QuizMode instance.

        Raises:
            ValueError: If the mode name is not recognised.
        """
        key = mode.strip().lower()
        cls = QuizModeFactory._MODES.get(key)
        if cls is None:
            valid = ", ".join(sorted(QuizModeFactory._MODES))
            raise ValueError(
                f"Unknown quiz mode '{mode}'. Valid options are: {valid}."
            )
        return cls()
