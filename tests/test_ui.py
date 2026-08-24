"""
Tests for the QuizSession UI layer in utils/ui.py.

All tests inject mock input/output callables to avoid terminal interaction.
"""

from unittest.mock import MagicMock

from utils.flashcard import Flashcard
from utils.quiz_engine import (
    AdaptiveMode,
    RandomMode,
    SequentialMode,
)
from utils.stats import SessionStats
from utils.ui import QuizSession


def make_cards(n: int) -> list:
    """Return a list of n distinct Flashcard objects."""
    return [Flashcard(front=f"Q{i}", back=f"A{i}") for i in range(n)]


def make_session(inputs, mode=None, stats=None):
    """Build a QuizSession with mocked I/O.

    Args:
        inputs: List of strings the mock input callable will return in order.
        mode: QuizMode instance (defaults to SequentialMode).
        stats: SessionStats instance (defaults to a fresh one).

    Returns:
        Tuple of (session, print_mock).
    """
    if mode is None:
        mode = SequentialMode()
    if stats is None:
        stats = SessionStats()
    input_iter = iter(inputs)
    input_mock = lambda prompt="": next(input_iter)  # noqa: E731
    print_mock = MagicMock()
    session = QuizSession(
        mode=mode, stats=stats, input_fn=input_mock, print_fn=print_mock
    )
    return session, print_mock


class TestAnswerChecking:

    def test_correct_answer_exact_match(self):
        session, _ = make_session(["A0"])
        mode = SequentialMode()
        stats = SessionStats()
        session = QuizSession(
            mode=mode,
            stats=stats,
            input_fn=lambda p="": "A0",
            print_fn=MagicMock(),
        )
        session.run(make_cards(1))
        assert stats.correct == 1
        assert stats.incorrect == 0

    def test_correct_answer_case_insensitive(self):
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": "a0",
            print_fn=MagicMock(),
        )
        session.run(make_cards(1))
        assert stats.correct == 1

    def test_correct_answer_strips_whitespace(self):
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": "  A0  ",
            print_fn=MagicMock(),
        )
        session.run(make_cards(1))
        assert stats.correct == 1

    def test_whitespace_only_answer_is_incorrect(self):
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": "   ",
            print_fn=MagicMock(),
        )
        session.run(make_cards(1))
        assert stats.incorrect == 1

    def test_incorrect_answer_updates_stats(self):
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": "wrong",
            print_fn=MagicMock(),
        )
        session.run(make_cards(1))
        assert stats.incorrect == 1
        assert stats.correct == 0

    def test_incorrect_answer_shows_correct_answer(self):
        print_mock = MagicMock()
        session = QuizSession(
            mode=SequentialMode(),
            stats=SessionStats(),
            input_fn=lambda p="": "wrong",
            print_fn=print_mock,
        )
        session.run([Flashcard("Q", "RightAnswer")])
        output = " ".join(str(c) for c in print_mock.call_args_list)
        assert "RightAnswer" in output


class TestExitCommand:

    def test_exit_ends_session(self):
        stats = SessionStats()
        session, _ = make_session(["exit"], stats=stats)
        session.run(make_cards(3))
        assert stats.total == 0

    def test_exit_case_insensitive(self):
        stats = SessionStats()
        session, _ = make_session(["EXIT"], stats=stats)
        session.run(make_cards(3))
        assert stats.total == 0

    def test_exit_prints_message(self):
        session, print_mock = make_session(["exit"])
        session.run(make_cards(1))
        output = " ".join(str(c) for c in print_mock.call_args_list)
        assert "ended" in output.lower() or "exit" in output.lower()


class TestSkipCommand:

    def test_skip_records_in_stats(self):
        stats = SessionStats()
        session, _ = make_session(["skip"], stats=stats)
        session.run(make_cards(1))
        assert stats.skipped == 1

    def test_skip_does_not_count_as_correct_or_incorrect(self):
        stats = SessionStats()
        session, _ = make_session(["skip"], stats=stats)
        session.run(make_cards(1))
        assert stats.correct == 0
        assert stats.incorrect == 0

    def test_skip_case_insensitive(self):
        stats = SessionStats()
        session, _ = make_session(["SKIP"], stats=stats)
        session.run(make_cards(1))
        assert stats.skipped == 1

    def test_skip_continues_to_next_card(self):
        stats = SessionStats()
        inputs = iter(["skip", "A1"])
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": next(inputs),
            print_fn=MagicMock(),
        )
        session.run(make_cards(2))
        assert stats.skipped == 1
        assert stats.correct == 1


class TestKeyboardInterrupt:

    def test_keyboard_interrupt_handled_gracefully(self):
        def raise_interrupt(p=""):
            raise KeyboardInterrupt

        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=raise_interrupt,
            print_fn=MagicMock(),
        )
        session.run(make_cards(3))
        assert stats.total == 0

    def test_keyboard_interrupt_prints_message(self):
        def raise_interrupt(p=""):
            raise KeyboardInterrupt

        print_mock = MagicMock()
        session = QuizSession(
            mode=SequentialMode(),
            stats=SessionStats(),
            input_fn=raise_interrupt,
            print_fn=print_mock,
        )
        session.run(make_cards(1))
        output = " ".join(str(c) for c in print_mock.call_args_list)
        assert "interrupt" in output.lower() or "exit" in output.lower()


class TestEmptyCards:

    def test_empty_cards_returns_stats(self):
        stats = SessionStats()
        session, print_mock = make_session([], stats=stats)
        result = session.run([])
        assert result is stats
        assert stats.total == 0

    def test_empty_cards_prints_message(self):
        session, print_mock = make_session([])
        session.run([])
        output = " ".join(str(c) for c in print_mock.call_args_list)
        assert "no" in output.lower() or "empty" in output.lower()


class TestStatsReturnedAfterSession:

    def test_run_returns_stats_instance(self):
        stats = SessionStats()
        session, _ = make_session(["A0"], stats=stats)
        result = session.run(make_cards(1))
        assert result is stats

    def test_stats_accessible_via_property(self):
        stats = SessionStats()
        session, _ = make_session(["A0"], stats=stats)
        assert session.stats is stats

    def test_final_summary_printed(self):
        session, print_mock = make_session(["A0"])
        session.run(make_cards(1))
        output = " ".join(str(c) for c in print_mock.call_args_list)
        assert "score" in output.lower() or "correct" in output.lower()


class TestSequentialModeIntegration:

    def test_sequential_all_correct(self):
        cards = make_cards(3)
        answers = iter([c.back for c in cards])
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": next(answers),
            print_fn=MagicMock(),
        )
        session.run(cards)
        assert stats.correct == 3
        assert stats.incorrect == 0

    def test_sequential_all_incorrect(self):
        cards = make_cards(3)
        stats = SessionStats()
        session = QuizSession(
            mode=SequentialMode(),
            stats=stats,
            input_fn=lambda p="": "wrong",
            print_fn=MagicMock(),
        )
        session.run(cards)
        assert stats.incorrect == 3


class TestRandomModeIntegration:

    def test_random_mode_all_cards_attempted(self):
        cards = make_cards(4)
        stats = SessionStats()
        session = QuizSession(
            mode=RandomMode(seed=42),
            stats=stats,
            input_fn=lambda p="": "wrong",
            print_fn=MagicMock(),
        )
        session.run(cards)
        assert stats.total_attempted == 4


class TestAdaptiveModeIntegration:

    def test_adaptive_receives_correct_result(self):
        card = Flashcard("Q", "A")
        mode = AdaptiveMode()
        stats = SessionStats()
        session = QuizSession(
            mode=mode,
            stats=stats,
            input_fn=lambda p="": "A",
            print_fn=MagicMock(),
        )
        session.run([card])
        assert stats.correct == 1
        assert mode.is_complete()

    def test_adaptive_receives_incorrect_result(self):
        card = Flashcard("Q", "A")
        mode = AdaptiveMode()
        stats = SessionStats()
        answers = iter(["wrong", "A"])
        session = QuizSession(
            mode=mode,
            stats=stats,
            input_fn=lambda p="": next(answers),
            print_fn=MagicMock(),
        )
        session.run([card])
        assert stats.incorrect == 1
        assert stats.correct == 1
        assert mode.is_complete()
