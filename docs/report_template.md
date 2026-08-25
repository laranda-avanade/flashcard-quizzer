# AI-Assisted Development Project Report

**Student Name:** Lance Aaron Aranda
**Project Title:** Flashcard Quizzer — Interactive CLI Quiz Tool
**Date:** August 2026

---

## Executive Summary

The Flashcard Quizzer is a command-line Python application that presents
flashcards stored in JSON files and quizzes the user through three distinct
modes: sequential, random, and adaptive. The adaptive mode tracks incorrect
answers and re-presents missed cards until the user answers them correctly,
providing a lightweight spaced-practice experience without external
dependencies.

Development used Claude as a collaborative assistant across six phases. Each
phase began with an architecture review before any code was written; the AI
generated initial implementations that the student reviewed, tested, and
corrected before authorising the next phase. All four reviewer verification
commands exit 0: `black --check .`, `flake8 .`, `mypy main.py utils/`, and
`pytest` (156 tests, greater than 80 percent coverage).

---

## Project Overview

### Problem Statement

Existing CLI flashcard tools often hardcode a single presentation order or
require complicated setup. This project built a minimal quizzer that reads
standard JSON files, supports multiple study strategies, and reports session
statistics without a database or web server.

### Solution Approach

The application is structured around the Strategy pattern for quiz modes and
a Factory for runtime mode selection. File I/O, statistics, and terminal
interaction are isolated in separate modules so each concern can be tested
independently. The technology stack is minimal: Python standard library plus
`colorama` for ANSI colour.

### Final Features

- Sequential, random, and adaptive quiz modes
- Dual JSON format support — flat array or wrapped `{"cards": [...]}`
- Session statistics with score percentage via `--stats` flag
- Coloured terminal feedback; `skip` and `exit` commands
- Descriptive error messages for missing files, malformed JSON, and unknown modes
- Graceful handling of `KeyboardInterrupt` and stdin `EOFError`
- Full type hints; passes `black --check .`, `flake8 .`, `mypy main.py utils/`

---

## AI Collaboration Experience

### Workflow

Claude (Anthropic) was the sole AI assistant used throughout; full records are
in `docs/ai_edit_log.md`. Each phase followed four steps: (1) read and
summarise existing files before proposing changes; (2) state which files would
change before making them; (3) run pytest and Flake8 immediately after
implementation; (4) review generated code before accepting.

### Key Interactions

**Architecture analysis — accepted with modification.** Claude proposed a
7-module design splitting strategies and factory into separate files. A
follow-up asking for justification led to the simpler `quiz_engine.py`. First-
pass AI architectures often over-separate concerns; asking for justification
produces leaner designs.

**AdaptiveMode algorithm bug — rejected and corrected.** The initial
implementation mutated `_current_retry_pass_size` mid-pass, allowing a card
answered incorrectly during a retry pass to be immediately re-consumed in the
same pass. A termination test exposed the defect; code review alone missed it.
Stateful queue algorithms require dedicated termination tests.

**Test assumption error — rejected.** A generated test asserted an adaptive
session terminates when every answer is always wrong — logically impossible.
Replaced with a realistic scenario. Generated test logic must be checked for
feasibility, not just syntax.

**Dependency injection design — accepted as-is.** Passing `input_fn` and
`print_fn` callables to `QuizSession` made the entire UI layer testable
without monkeypatching.

### Challenges with AI Collaboration

AI excelled at boilerplate, type-annotated implementations, and test
scaffolding, but struggled with stateful queue algorithms and made optimistic
test assumptions. Requiring the AI to state intended file changes before making
them prevented scope creep. Running the full test suite immediately after each
implementation pass was the most effective way to catch issues while context
was fresh.

---

## Software Engineering Practices

### Code Quality

All Python files pass:

- `black --check .` — formatted at 79-character line length via `pyproject.toml`
- `flake8 .` — zero violations via `setup.cfg`
- `mypy main.py utils/` — zero errors; requires `types-colorama` from `requirements.txt`
- `isort` — import ordering

Type hints are present on all public functions and methods.

### Testing Strategy

| Test file | Key scenarios |
|---|---|
| `test_flashcard_loader.py` | Flat list, wrapped format, missing file, malformed JSON, empty/invalid cards |
| `test_quiz_modes.py` | Sequential order, random shuffle, adaptive retry and termination, factory |
| `test_stats.py` | Counts, score percentage, division by zero, reset |
| `test_ui.py` | Correct/incorrect/skip/exit/EOF flows, empty deck, keyboard interrupt |
| `test_main.py` | Full CLI integration, bad file, bad mode, stats flag |

156 tests pass with greater than 80 percent coverage.

---

## Design Patterns

`QuizMode` is an abstract base class in `utils/quiz_engine.py` defining a
four-method interface. `SequentialMode`, `RandomMode`, and `AdaptiveMode` each
implement this interface with a different ordering algorithm. `QuizSession`
holds the active mode and delegates all card-ordering decisions to it; adding
a new mode requires only a new subclass. Without the Strategy pattern, the
session would contain a conditional block for every mode, making each algorithm
harder to test in isolation.

`QuizModeFactory.create()` maps mode-name strings to concrete classes,
normalises input, and raises a descriptive `ValueError` on unknown names.
`main.py` has no direct dependency on any concrete mode class, keeping object-
creation logic and input validation centralised. Full Udacity template
documentation is in `docs/design_patterns.md`.

---

## Technical Challenges and Solutions

### AdaptiveMode Termination Guarantee

The retry pass mechanism (`_current_retry_pass_size`) tracks the queue size at
the start of each pass. Cards re-enqueued during a pass are deferred to the
next pass; the current pass size is never mutated after it is set. Without
this constraint, a card answered incorrectly during an active pass is
immediately re-consumed, creating an unbounded loop. The defect was identified
by a termination test — code review alone did not catch it.

### Dual JSON Format Support

`FileHandler.load_flashcards` inspects the parsed JSON type: bare lists are
used directly; dicts with a `"cards"` key have the list extracted; any other
structure raises a descriptive `ValueError`. Claude proposed this detection
approach on the first pass; no modification was required.

---

## Reflection

### What Worked Well

The phased approach — inspect, specify, implement, verify — produced reliable
results. Each phase delivered working, tested, linted code before the next
phase began, so there was no accumulated technical debt. The dependency
injection design in `QuizSession` was particularly effective: it made the UI
layer fully testable without any monkeypatching or subprocess calls.

### What I Learned

Implementing Strategy and Factory in a real project made their trade-offs
concrete. The adaptive mode's algorithm is more complex than strictly
necessary — a simpler two-pass model would be easier to test — but it handles
edge cases correctly and the extra complexity was justified. The clearest
lesson from AI collaboration: its value scales with specification precision.
Vague prompts produced over-engineered designs; precise prompts with explicit
contracts produced correct implementations that needed minimal correction.

### Future Enhancements

- Spaced repetition mode (SM-2 algorithm) as a fourth `QuizMode` strategy,
  demonstrating that the Strategy pattern makes the extension trivial
- Persistent progress tracking across sessions using `FileHandler`
- A `--reverse` flag to quiz from the back side of each card
- Batch statistics export to JSON for progress visualisation

---

## Conclusion

The Flashcard Quizzer demonstrated that AI-assisted development produces high-
quality, maintainable Python when the developer maintains ownership of
architecture, contracts, and quality gates. Claude accelerated implementation
significantly, but every non-trivial deliverable required human review to catch
algorithm bugs and fix test assumptions. The value of an AI assistant scales
directly with the precision of the specification — a lesson that will carry
forward into future projects.

---

## Appendices

### Appendix A: AI Interaction Log

Full interaction records are in `docs/ai_edit_log.md`.

### Appendix B: Code Statistics

- **Total tests:** 156 passing, 0 failing
- **Flake8 violations:** 0
- **mypy errors:** 0 (with `types-colorama` installed)
- **Black compliance:** all files formatted at 79-character line length

### Appendix C: Resources

- Python `abc` module documentation — abstract base classes
- Gang of Four: *Design Patterns: Elements of Reusable Object-Oriented Software*
- pytest documentation — fixtures, parametrize, monkeypatch
- mypy documentation — type checking with abstract base classes
