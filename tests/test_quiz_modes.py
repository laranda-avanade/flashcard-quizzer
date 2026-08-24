"""
Tests for quiz engine: SequentialMode, RandomMode, AdaptiveMode,
and QuizModeFactory.
"""

import pytest

from utils.flashcard import Flashcard
from utils.quiz_engine import (
    AdaptiveMode,
    QuizMode,
    QuizModeFactory,
    RandomMode,
    SequentialMode,
)


def make_cards(n: int) -> list:
    """Return a list of n distinct Flashcard objects."""
    return [Flashcard(front=f"Q{i}", back=f"A{i}") for i in range(n)]


class TestSequentialMode:

    def test_returns_cards_in_original_order(self):
        cards = make_cards(4)
        mode = SequentialMode()
        mode.start(cards)
        result = []
        while not mode.is_complete():
            result.append(mode.next_card())
        assert result == cards

    def test_each_card_presented_exactly_once(self):
        cards = make_cards(5)
        mode = SequentialMode()
        mode.start(cards)
        result = []
        while not mode.is_complete():
            result.append(mode.next_card())
        assert len(result) == 5
        assert sorted(result, key=lambda c: c.front) == sorted(
            cards, key=lambda c: c.front
        )

    def test_next_card_returns_none_when_complete(self):
        cards = make_cards(2)
        mode = SequentialMode()
        mode.start(cards)
        mode.next_card()
        mode.next_card()
        assert mode.next_card() is None

    def test_is_complete_initially_false(self):
        mode = SequentialMode()
        mode.start(make_cards(1))
        assert not mode.is_complete()

    def test_is_complete_true_after_all_cards(self):
        cards = make_cards(3)
        mode = SequentialMode()
        mode.start(cards)
        for _ in cards:
            mode.next_card()
        assert mode.is_complete()

    def test_record_answer_does_not_affect_order(self):
        cards = make_cards(3)
        mode = SequentialMode()
        mode.start(cards)
        first = mode.next_card()
        mode.record_answer(first, correct=False)
        second = mode.next_card()
        assert second == cards[1]

    def test_empty_deck_is_immediately_complete(self):
        mode = SequentialMode()
        mode.start([])
        assert mode.is_complete()
        assert mode.next_card() is None


class TestRandomMode:

    def test_includes_every_card_exactly_once(self):
        cards = make_cards(6)
        mode = RandomMode(seed=0)
        mode.start(cards)
        result = []
        while not mode.is_complete():
            result.append(mode.next_card())
        assert len(result) == 6
        assert sorted(result, key=lambda c: c.front) == sorted(
            cards, key=lambda c: c.front
        )

    def test_order_differs_from_original(self):
        cards = make_cards(10)
        mode = RandomMode(seed=42)
        mode.start(cards)
        result = []
        while not mode.is_complete():
            result.append(mode.next_card())
        assert result != cards

    def test_deterministic_with_same_seed(self):
        cards = make_cards(8)
        mode_a = RandomMode(seed=7)
        mode_a.start(cards)
        result_a = []
        while not mode_a.is_complete():
            result_a.append(mode_a.next_card())

        mode_b = RandomMode(seed=7)
        mode_b.start(cards)
        result_b = []
        while not mode_b.is_complete():
            result_b.append(mode_b.next_card())

        assert result_a == result_b

    def test_different_seeds_produce_different_orders(self):
        cards = make_cards(10)
        mode_a = RandomMode(seed=1)
        mode_a.start(cards)
        result_a = [mode_a.next_card() for _ in cards]

        mode_b = RandomMode(seed=2)
        mode_b.start(cards)
        result_b = [mode_b.next_card() for _ in cards]

        assert result_a != result_b

    def test_next_card_returns_none_when_complete(self):
        cards = make_cards(2)
        mode = RandomMode(seed=0)
        mode.start(cards)
        mode.next_card()
        mode.next_card()
        assert mode.next_card() is None

    def test_empty_deck_is_immediately_complete(self):
        mode = RandomMode()
        mode.start([])
        assert mode.is_complete()


class TestAdaptiveMode:

    def _run_session(self, mode, correct_on_first=True):
        """Drive a session, marking every answer correct on first encounter."""
        seen = set()
        results = []
        while not mode.is_complete():
            card = mode.next_card()
            if card is None:
                break
            first_time = id(card) not in seen
            seen.add(id(card))
            correct = correct_on_first and first_time
            mode.record_answer(card, correct=correct)
            results.append((card, correct))
        return results

    def test_presents_all_cards_when_all_correct(self):
        cards = make_cards(4)
        mode = AdaptiveMode()
        mode.start(cards)
        results = self._run_session(mode, correct_on_first=True)
        presented = [c for c, _ in results]
        assert sorted(presented, key=lambda c: c.front) == sorted(
            cards, key=lambda c: c.front
        )
        assert mode.is_complete()

    def test_repeats_incorrectly_answered_card(self):
        cards = make_cards(3)
        mode = AdaptiveMode()
        mode.start(cards)

        answers = {id(c): False for c in cards}
        answers[id(cards[2])] = True

        seen_counts = {}
        while not mode.is_complete():
            card = mode.next_card()
            if card is None:
                break
            seen_counts[id(card)] = seen_counts.get(id(card), 0) + 1
            correct = answers[id(card)]
            if not correct:
                answers[id(card)] = True
            mode.record_answer(card, correct=correct)

        assert seen_counts[id(cards[0])] == 2
        assert seen_counts[id(cards[1])] == 2
        assert seen_counts[id(cards[2])] == 1

    def test_stops_repeating_after_correct_answer(self):
        cards = make_cards(1)
        mode = AdaptiveMode()
        mode.start(cards)

        card = mode.next_card()
        mode.record_answer(card, correct=False)

        card2 = mode.next_card()
        assert card2 == cards[0]
        mode.record_answer(card2, correct=True)

        assert mode.is_complete()
        assert mode.next_card() is None

    def test_terminates_without_infinite_loop(self):
        cards = make_cards(5)
        mode = AdaptiveMode()
        mode.start(cards)

        wrong_remaining = {id(c): 2 for c in cards}
        max_iterations = 1000
        iterations = 0
        while not mode.is_complete():
            card = mode.next_card()
            if card is None:
                break
            if wrong_remaining[id(card)] > 0:
                wrong_remaining[id(card)] -= 1
                mode.record_answer(card, correct=False)
            else:
                mode.record_answer(card, correct=True)
            iterations += 1
            if iterations > max_iterations:
                pytest.fail("AdaptiveMode did not terminate within limit.")

        assert mode.is_complete()

    def test_is_complete_when_deck_and_retry_empty(self):
        cards = make_cards(2)
        mode = AdaptiveMode()
        mode.start(cards)
        for card in cards:
            c = mode.next_card()
            mode.record_answer(c, correct=True)
        assert mode.is_complete()

    def test_empty_deck_is_immediately_complete(self):
        mode = AdaptiveMode()
        mode.start([])
        assert mode.is_complete()
        assert mode.next_card() is None


class TestQuizModeFactory:

    def test_creates_sequential_mode(self):
        mode = QuizModeFactory.create("sequential")
        assert isinstance(mode, SequentialMode)

    def test_creates_random_mode(self):
        mode = QuizModeFactory.create("random")
        assert isinstance(mode, RandomMode)

    def test_creates_adaptive_mode(self):
        mode = QuizModeFactory.create("adaptive")
        assert isinstance(mode, AdaptiveMode)

    def test_case_insensitive(self):
        assert isinstance(QuizModeFactory.create("Sequential"), SequentialMode)
        assert isinstance(QuizModeFactory.create("RANDOM"), RandomMode)
        assert isinstance(QuizModeFactory.create("Adaptive"), AdaptiveMode)

    def test_whitespace_trimmed(self):
        mode = QuizModeFactory.create("  sequential  ")
        assert isinstance(mode, SequentialMode)

    def test_invalid_mode_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown quiz mode"):
            QuizModeFactory.create("nonexistent")

    def test_invalid_mode_error_lists_valid_options(self):
        with pytest.raises(ValueError, match="sequential"):
            QuizModeFactory.create("bad_mode")

    def test_returns_quiz_mode_instance(self):
        for name in ("sequential", "random", "adaptive"):
            assert isinstance(QuizModeFactory.create(name), QuizMode)
