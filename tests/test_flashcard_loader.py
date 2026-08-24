"""
Tests for flashcard loading and validation in FileHandler.load_flashcards
and the Flashcard dataclass.
"""

import json
import os
import tempfile

import pytest

from utils.file_handler import FileHandler
from utils.flashcard import Flashcard


class TestFlashcard:
    """Tests for the Flashcard dataclass validation."""

    def test_valid_flashcard(self):
        card = Flashcard(front="Question", back="Answer")
        assert card.front == "Question"
        assert card.back == "Answer"

    def test_empty_front_raises(self):
        with pytest.raises(ValueError, match="front"):
            Flashcard(front="", back="Answer")

    def test_whitespace_front_raises(self):
        with pytest.raises(ValueError, match="front"):
            Flashcard(front="   ", back="Answer")

    def test_empty_back_raises(self):
        with pytest.raises(ValueError, match="back"):
            Flashcard(front="Question", back="")

    def test_whitespace_back_raises(self):
        with pytest.raises(ValueError, match="back"):
            Flashcard(front="Question", back="   ")

    def test_non_string_front_raises(self):
        with pytest.raises(ValueError, match="front"):
            Flashcard(front=42, back="Answer")  # type: ignore

    def test_non_string_back_raises(self):
        with pytest.raises(ValueError, match="back"):
            Flashcard(front="Question", back=None)  # type: ignore


class TestLoadFlashcards:
    """Tests for FileHandler.load_flashcards."""

    def _write_json(self, data) -> str:
        """Write data to a temp JSON file and return the path."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def _write_raw(self, text: str) -> str:
        """Write raw text to a temp file and return the path."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_load_flat_list_format(self):
        path = self._write_json(
            [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]
        )
        cards = FileHandler.load_flashcards(path)
        assert len(cards) == 2
        assert cards[0] == Flashcard("Q1", "A1")
        assert cards[1] == Flashcard("Q2", "A2")
        os.unlink(path)

    def test_load_wrapped_cards_format(self):
        path = self._write_json(
            {"cards": [{"front": "Q1", "back": "A1"}]}
        )
        cards = FileHandler.load_flashcards(path)
        assert len(cards) == 1
        assert cards[0] == Flashcard("Q1", "A1")
        os.unlink(path)

    def test_load_sample_file(self):
        sample = os.path.join(
            os.path.dirname(__file__), "..", "data", "sample_cards.json"
        )
        cards = FileHandler.load_flashcards(sample)
        assert len(cards) == 5
        assert all(isinstance(c, Flashcard) for c in cards)

    def test_load_file_not_found(self):
        with pytest.raises(FileNotFoundError, match="not found"):
            FileHandler.load_flashcards("/nonexistent/path/cards.json")

    def test_load_malformed_json(self):
        path = self._write_raw("{not valid json")
        with pytest.raises(ValueError, match="Malformed JSON"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_empty_cards_list(self):
        path = self._write_json([])
        with pytest.raises(ValueError, match="No flashcards found"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_empty_cards_key(self):
        path = self._write_json({"cards": []})
        with pytest.raises(ValueError, match="No flashcards found"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_wrong_top_level_type_string(self):
        path = self._write_json("just a string")
        with pytest.raises(ValueError, match="must be a JSON array"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_wrong_top_level_type_number(self):
        path = self._write_json(42)
        with pytest.raises(ValueError, match="must be a JSON array"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_dict_without_cards_key(self):
        path = self._write_json({"data": []})
        with pytest.raises(ValueError, match="must be a JSON array"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_cards_not_a_list(self):
        path = self._write_json({"cards": "not a list"})
        with pytest.raises(ValueError, match="must be a list"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_missing_front_key(self):
        path = self._write_json([{"back": "Answer"}])
        with pytest.raises(ValueError, match="missing the 'front' key"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_missing_back_key(self):
        path = self._write_json([{"front": "Question"}])
        with pytest.raises(ValueError, match="missing the 'back' key"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_empty_front_value(self):
        path = self._write_json([{"front": "", "back": "Answer"}])
        with pytest.raises(ValueError, match="index 0"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_empty_back_value(self):
        path = self._write_json([{"front": "Question", "back": ""}])
        with pytest.raises(ValueError, match="index 0"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_non_string_front(self):
        path = self._write_json([{"front": 123, "back": "Answer"}])
        with pytest.raises(ValueError, match="index 0"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_non_string_back(self):
        path = self._write_json([{"front": "Question", "back": None}])
        with pytest.raises(ValueError, match="index 0"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_load_non_dict_card(self):
        path = self._write_json(["not a dict"])
        with pytest.raises(ValueError, match="index 0 must be an object"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_error_reports_correct_index(self):
        path = self._write_json(
            [
                {"front": "Good Q", "back": "Good A"},
                {"front": "", "back": "Answer"},
            ]
        )
        with pytest.raises(ValueError, match="index 1"):
            FileHandler.load_flashcards(path)
        os.unlink(path)

    def test_extra_fields_in_card_are_ignored(self):
        path = self._write_json(
            [{"front": "Q", "back": "A", "difficulty": "hard"}]
        )
        cards = FileHandler.load_flashcards(path)
        assert cards[0] == Flashcard("Q", "A")
        os.unlink(path)
