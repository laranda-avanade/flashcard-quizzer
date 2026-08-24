"""
Tests for the main.py CLI entry point.
"""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from main import build_parser, main


def write_json_file(data) -> str:
    """Write data to a temp JSON file and return the path."""
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return path


VALID_CARDS = [
    {"front": "What is 2+2?", "back": "4"},
    {"front": "Capital of France?", "back": "Paris"},
]


class TestBuildParser:

    def test_file_argument_required(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_file_argument_accepted(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json"])
        assert args.file == "cards.json"

    def test_mode_defaults_to_sequential(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json"])
        assert args.mode == "sequential"

    def test_mode_argument_accepted(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json", "-m", "random"])
        assert args.mode == "random"

    def test_stats_flag_defaults_false(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json"])
        assert args.stats is False

    def test_stats_flag_set_when_passed(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json", "--stats"])
        assert args.stats is True

    def test_long_form_file_argument(self):
        parser = build_parser()
        args = parser.parse_args(["--file", "cards.json"])
        assert args.file == "cards.json"

    def test_long_form_mode_argument(self):
        parser = build_parser()
        args = parser.parse_args(["-f", "cards.json", "--mode", "adaptive"])
        assert args.mode == "adaptive"


class TestMainSuccessfulRun:

    def test_sequential_mode_runs_successfully(self):
        path = write_json_file(VALID_CARDS)
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path, "-m", "sequential"])
            assert result == 0
        finally:
            os.unlink(path)

    def test_random_mode_runs_successfully(self):
        path = write_json_file(VALID_CARDS)
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path, "-m", "random"])
            assert result == 0
        finally:
            os.unlink(path)

    def test_adaptive_mode_runs_successfully(self):
        path = write_json_file(VALID_CARDS)
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path, "-m", "adaptive"])
            assert result == 0
        finally:
            os.unlink(path)

    def test_default_mode_is_sequential(self):
        path = write_json_file(VALID_CARDS)
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path])
            assert result == 0
        finally:
            os.unlink(path)

    def test_stats_flag_prints_summary(self, capsys):
        path = write_json_file(VALID_CARDS)
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path, "--stats"])
            assert result == 0
            captured = capsys.readouterr()
            assert "Score" in captured.out or "Correct" in captured.out
        finally:
            os.unlink(path)


class TestMainErrorPaths:

    def test_missing_file_returns_exit_code_1(self):
        result = main(["-f", "/nonexistent/path/cards.json"])
        assert result == 1

    def test_missing_file_prints_error(self, capsys):
        main(["-f", "/nonexistent/path/cards.json"])
        captured = capsys.readouterr()
        err = captured.err.lower()
        assert "error" in err or "not found" in err

    def test_malformed_json_returns_exit_code_1(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            f.write("{not valid json")
        try:
            result = main(["-f", path])
            assert result == 1
        finally:
            os.unlink(path)

    def test_invalid_mode_returns_exit_code_1(self):
        path = write_json_file(VALID_CARDS)
        try:
            result = main(["-f", path, "-m", "nonexistent_mode"])
            assert result == 1
        finally:
            os.unlink(path)

    def test_invalid_mode_prints_error(self, capsys):
        path = write_json_file(VALID_CARDS)
        try:
            main(["-f", path, "-m", "nonexistent_mode"])
            captured = capsys.readouterr()
            assert "error" in captured.err.lower()
        finally:
            os.unlink(path)

    def test_empty_cards_file_returns_exit_code_1(self):
        path = write_json_file([])
        try:
            result = main(["-f", path])
            assert result == 1
        finally:
            os.unlink(path)

    def test_wrapped_format_loads_correctly(self):
        path = write_json_file({"cards": VALID_CARDS})
        try:
            with patch("utils.ui.QuizSession.run") as mock_run:
                mock_run.return_value = MagicMock()
                result = main(["-f", path])
            assert result == 0
        finally:
            os.unlink(path)
