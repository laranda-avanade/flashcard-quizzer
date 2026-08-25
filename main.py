"""
Flashcard Quizzer - CLI entry point.

Usage:
    python main.py -f <file> [-m <mode>] [--stats]

Arguments:
    -f / --file   Path to a JSON flashcard file (required)
    -m / --mode   Quiz mode: sequential, random, adaptive (default: sequential)
    --stats       Print session statistics after the quiz
"""

import argparse
import sys

from utils.file_handler import FileHandler
from utils.quiz_engine import QuizModeFactory
from utils.stats import SessionStats
from utils.ui import QuizSession


def build_parser() -> argparse.ArgumentParser:
    """Return a configured argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Flashcard Quizzer - an interactive flashcard quiz tool.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        metavar="FILE",
        help="Path to a JSON flashcard file.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        default="sequential",
        metavar="MODE",
        help=(
            "Quiz mode: sequential, random, or adaptive "
            "(default: sequential)."
        ),
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display session statistics after the quiz.",
    )
    return parser


def main(argv=None) -> int:
    """Run the Flashcard Quizzer CLI.

    Args:
        argv: Argument list (defaults to sys.argv when None).

    Returns:
        Exit code: 0 on success, 1 on error.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        cards = FileHandler.load_flashcards(args.file)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        mode = QuizModeFactory.create(args.mode)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    stats = SessionStats()
    session = QuizSession(mode=mode, stats=stats)

    session.run(cards)

    if args.stats:
        print(f"\n{stats.summary()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
