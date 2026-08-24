"""
Tests for SessionStats in utils/stats.py.
"""

import pytest

from utils.stats import SessionStats


class TestSessionStatsInitial:
    """SessionStats starts with all counters at zero."""

    def setup_method(self):
        self.stats = SessionStats()

    def test_initial_correct_is_zero(self):
        assert self.stats.correct == 0

    def test_initial_incorrect_is_zero(self):
        assert self.stats.incorrect == 0

    def test_initial_skipped_is_zero(self):
        assert self.stats.skipped == 0

    def test_initial_total_attempted_is_zero(self):
        assert self.stats.total_attempted == 0

    def test_initial_total_is_zero(self):
        assert self.stats.total == 0

    def test_initial_score_percentage_is_zero(self):
        assert self.stats.score_percentage == 0.0


class TestRecordCorrect:

    def setup_method(self):
        self.stats = SessionStats()

    def test_record_correct_increments_by_one(self):
        self.stats.record_correct()
        assert self.stats.correct == 1

    def test_record_correct_multiple_calls(self):
        self.stats.record_correct()
        self.stats.record_correct()
        self.stats.record_correct()
        assert self.stats.correct == 3

    def test_record_correct_with_count(self):
        self.stats.record_correct(count=5)
        assert self.stats.correct == 5

    def test_record_correct_zero_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_correct(count=0)

    def test_record_correct_negative_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_correct(count=-1)

    def test_record_correct_updates_total_attempted(self):
        self.stats.record_correct(count=3)
        assert self.stats.total_attempted == 3

    def test_record_correct_updates_total(self):
        self.stats.record_correct(count=2)
        assert self.stats.total == 2


class TestRecordIncorrect:

    def setup_method(self):
        self.stats = SessionStats()

    def test_record_incorrect_increments_by_one(self):
        self.stats.record_incorrect()
        assert self.stats.incorrect == 1

    def test_record_incorrect_multiple_calls(self):
        self.stats.record_incorrect()
        self.stats.record_incorrect()
        assert self.stats.incorrect == 2

    def test_record_incorrect_with_count(self):
        self.stats.record_incorrect(count=4)
        assert self.stats.incorrect == 4

    def test_record_incorrect_zero_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_incorrect(count=0)

    def test_record_incorrect_negative_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_incorrect(count=-3)

    def test_record_incorrect_updates_total_attempted(self):
        self.stats.record_incorrect(count=2)
        assert self.stats.total_attempted == 2

    def test_record_incorrect_updates_total(self):
        self.stats.record_incorrect(count=2)
        assert self.stats.total == 2


class TestRecordSkipped:

    def setup_method(self):
        self.stats = SessionStats()

    def test_record_skipped_increments_by_one(self):
        self.stats.record_skipped()
        assert self.stats.skipped == 1

    def test_record_skipped_multiple_calls(self):
        self.stats.record_skipped()
        self.stats.record_skipped()
        assert self.stats.skipped == 2

    def test_record_skipped_with_count(self):
        self.stats.record_skipped(count=3)
        assert self.stats.skipped == 3

    def test_record_skipped_zero_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_skipped(count=0)

    def test_record_skipped_negative_raises(self):
        with pytest.raises(ValueError):
            self.stats.record_skipped(count=-1)

    def test_skipped_does_not_affect_total_attempted(self):
        self.stats.record_skipped(count=5)
        assert self.stats.total_attempted == 0

    def test_skipped_included_in_total(self):
        self.stats.record_skipped(count=5)
        assert self.stats.total == 5


class TestScorePercentage:

    def setup_method(self):
        self.stats = SessionStats()

    def test_score_zero_when_no_attempts(self):
        assert self.stats.score_percentage == 0.0

    def test_score_100_when_all_correct(self):
        self.stats.record_correct(count=5)
        assert self.stats.score_percentage == 100.0

    def test_score_0_when_all_incorrect(self):
        self.stats.record_incorrect(count=5)
        assert self.stats.score_percentage == 0.0

    def test_score_50_percent(self):
        self.stats.record_correct(count=5)
        self.stats.record_incorrect(count=5)
        assert self.stats.score_percentage == 50.0

    def test_score_75_percent(self):
        self.stats.record_correct(count=3)
        self.stats.record_incorrect(count=1)
        assert self.stats.score_percentage == 75.0

    def test_skipped_excluded_from_score(self):
        self.stats.record_correct(count=2)
        self.stats.record_incorrect(count=2)
        self.stats.record_skipped(count=10)
        assert self.stats.score_percentage == 50.0

    def test_score_is_float(self):
        self.stats.record_correct(count=1)
        assert isinstance(self.stats.score_percentage, float)


class TestTotals:

    def setup_method(self):
        self.stats = SessionStats()

    def test_total_attempted_correct_plus_incorrect(self):
        self.stats.record_correct(count=3)
        self.stats.record_incorrect(count=2)
        self.stats.record_skipped(count=4)
        assert self.stats.total_attempted == 5

    def test_total_includes_all_three(self):
        self.stats.record_correct(count=3)
        self.stats.record_incorrect(count=2)
        self.stats.record_skipped(count=4)
        assert self.stats.total == 9


class TestReset:

    def test_reset_clears_all_counters(self):
        stats = SessionStats()
        stats.record_correct(count=5)
        stats.record_incorrect(count=3)
        stats.record_skipped(count=2)
        stats.reset()
        assert stats.correct == 0
        assert stats.incorrect == 0
        assert stats.skipped == 0
        assert stats.total_attempted == 0
        assert stats.score_percentage == 0.0

    def test_reset_allows_reuse(self):
        stats = SessionStats()
        stats.record_correct(count=10)
        stats.reset()
        stats.record_correct(count=2)
        assert stats.correct == 2


class TestSummary:

    def test_summary_returns_string(self):
        stats = SessionStats()
        assert isinstance(stats.summary(), str)

    def test_summary_contains_correct_count(self):
        stats = SessionStats()
        stats.record_correct(count=4)
        assert "4" in stats.summary()

    def test_summary_contains_score(self):
        stats = SessionStats()
        stats.record_correct(count=1)
        assert "100.0%" in stats.summary()

    def test_summary_zero_state(self):
        stats = SessionStats()
        summary = stats.summary()
        assert "0" in summary
        assert "0.0%" in summary
