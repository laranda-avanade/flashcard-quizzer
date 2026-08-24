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

Development followed a six-phase plan in which Claude was used as a
collaborative coding assistant throughout. Every phase began with an
architecture review session before any code was written. The AI generated
initial implementations for all core modules; the student reviewed, tested,
and corrected each deliverable before authorising the next phase. The result
is a fully tested, linted, and type-checked application with 156 passing
tests and zero Flake8 or mypy violations.

The project demonstrates two Gang-of-Four design patterns (Strategy and
Factory), separation of concerns across six modules, dependency injection in
the UI layer, and a test suite that achieves greater than 80 percent coverage
across all application modules.

---

## Project Overview

### Problem Statement

Flashcard-based study tools are widely used for vocabulary, facts, and
concept review. Existing CLI tools often hardcode a single presentation order
or require complicated setup. This project aimed to build a minimal, easy-to-
extend CLI quizzer that reads standard JSON files, supports multiple study
strategies, and reports session statistics — all without requiring a database
or web server.

### Solution Approach

The application is structured around the Strategy pattern, which allows the
quiz engine to swap ordering algorithms at runtime without modifying the
session or UI code. A Factory class translates the CLI `--mode` argument into
the correct strategy object. File I/O is isolated in `FileHandler`, statistics
tracking in `SessionStats`, and terminal interaction in `QuizSession`, so each
concern can be tested independently.

The technology stack is intentionally minimal: the Python standard library
covers argument parsing, JSON loading, and data structures; `colorama` adds
cross-platform ANSI colour; `pytest` handles testing. No database, no external
API, and no framework dependencies.

### Final Features

- Sequential quiz mode — presents every card exactly once in original order
- Random quiz mode — shuffles cards with an optional seed for reproducibility
- Adaptive quiz mode — re-queues missed cards until all are answered correctly
- Dual JSON format support — flat list `[{...}]` or wrapped `{"cards": [...]}`
- Session statistics — correct, incorrect, skipped counts and score percentage
- Coloured terminal feedback — green for correct, red for incorrect answers
- Skip and exit commands — user can skip a card or quit mid-session
- Descriptive error messages — file-not-found, malformed JSON, unknown mode
- Type-checked codebase — passes mypy with `--check-untyped-defs`
- Linted and formatted — passes Flake8 at 79 characters and Black formatting

---

## AI Collaboration Experience

### AI Tools Used

Claude (Anthropic) was the sole AI assistant used throughout the project. All
interactions are documented in `docs/ai_edit_log.md`.

### Collaboration Workflow

Each development phase followed a consistent four-step workflow:

1. **Inspect before writing.** The AI was asked to read and summarise existing
   files before proposing any changes. This prevented unnecessary rewrites and
   surfaced reusable components in the starter codebase.
2. **State changes before making them.** Before editing any file, the AI was
   required to list exactly which files would change and why. This made every
   session auditable.
3. **Run tools and report results.** After implementation, the AI ran pytest
   and Flake8 and reported the output in the conversation. Failures were
   resolved in the same session before moving to the next phase.
4. **Review before accepting.** AI-generated code was not accepted until the
   student had read it, run the tests, and confirmed there were no logic errors
   or security issues.

### AI Interaction Examples

#### Interaction 1: Architecture Analysis (Accepted with Modification)

**Context:** The starter repository contained a generic Task Manager demo. The
first task was to understand the starter code and propose an architecture for
the Flashcard Quizzer before writing any application code.

**Prompt:** *"Inspect the existing repository and provide a summary of each
file, missing components, a proposed modular architecture, and potential
technical risks."*

**AI Response:** Claude proposed a 7-module architecture that split quiz
strategies and the factory into separate files (`quiz_modes.py` and
`quiz_factory.py`). It identified seven technical risks including adaptive mode
termination and testing random mode without a seed.

**Modification:** The 7-module design was rejected as over-engineered. A
follow-up prompt asked Claude to justify consolidation, and it agreed that a
single `quiz_engine.py` file was sufficient for the application's scale.

**Lesson learned:** The first architecture proposed by an AI often over-
separates concerns. Asking for justification of each module boundary produces
a leaner design.

#### Interaction 2: AdaptiveMode Algorithm Bug (Rejected and Corrected)

**Context:** After Phase 2 implementation, the adaptive mode had a subtle
infinite-loop risk. The initial `record_answer` implementation incremented
`_current_retry_pass_size` when a card was re-enqueued during an active retry
pass, allowing a card answered incorrectly during a retry pass to be
immediately re-consumed within the same pass.

**AI Response:** Claude's initial implementation looked correct in isolation
but failed under a systematic termination test.

**Correction:** The fix was to never mutate `_current_retry_pass_size` mid-
pass. Re-enqueued cards are always appended behind the current pass boundary
and deferred to the next pass. The corrected implementation was verified with
a test that drives the session with every card answered incorrectly a fixed
number of times before a final correct answer.

**Lesson learned:** AI-generated algorithms that maintain stateful queues
require dedicated termination tests. Structural code review alone is
insufficient — the defect was not visible from reading the code.

#### Interaction 3: Test Assumption Error (Rejected)

**Context:** One AI-generated test asserted that an adaptive session would
terminate even when every answer was always wrong.

**Why it was rejected:** That assumption is logically impossible. A card
answered incorrectly is re-enqueued; if every answer is always wrong, the
retry queue grows without bound and the session never terminates.

**Replacement:** The test was rewritten to use a realistic scenario — each
card is answered incorrectly a fixed number of times before being answered
correctly — which correctly validates termination under normal conditions.

**Lesson learned:** AI test generation sometimes makes optimistic assumptions
about program behaviour. Each generated test must be read for logical
consistency, not just syntax correctness.

#### Interaction 4: Flake8 Self-Correction (Accepted)

**Context:** After Phase 1 implementation, the AI ran Flake8 as part of the
verification step and found four violations: two E501 long lines in docstrings,
five W293 blank lines containing whitespace inherited from the starter file,
and one W292 missing final newline.

**AI Response:** Claude identified all violations, corrected them in the same
session without re-generating whole files, and re-ran Flake8 to confirm the
baseline was clean.

**Lesson learned:** Requiring the AI to run linting tools as part of the
implementation step — rather than as a final quality pass — catches style
issues while context is fresh and makes them trivial to fix.

#### Interaction 5: Dependency Injection Design (Accepted)

**Context:** The `QuizSession` class needed to be testable without a real
terminal. The AI proposed passing `input_fn` and `print_fn` callables as
constructor arguments so tests could inject mock functions.

**Accepted as-is:** The dependency injection approach was immediately correct.
Tests in `tests/test_ui.py` pass lists of pre-set answers as `input_fn` and
capture printed output via a list-appending `print_fn`, enabling full session
testing without any monkeypatching.

**Lesson learned:** Asking the AI to design for testability from the start
produces cleaner interfaces than retrofitting test hooks onto existing classes.

---

## Software Engineering Practices

### Code Quality

All Python files pass:

- **Black** formatting at 79-character line length
- **Flake8** linting with zero violations
- **mypy** type checking with `--check-untyped-defs`
- **isort** import ordering

Type hints are present on all public functions and methods. Docstrings follow
Google style and are present on every public class and method.

### Testing Strategy

The test suite contains 156 tests organised by module:

| Test file | Module under test | Key scenarios covered |
|---|---|---|
| `test_flashcard_loader.py` | `FileHandler.load_flashcards` | Flat list, wrapped format, missing file, malformed JSON, empty cards, invalid card fields |
| `test_file_handler.py` | `FileHandler` | CRUD operations, file existence, list files |
| `test_quiz_modes.py` | `quiz_engine` | Sequential order, random shuffle, adaptive retry, factory creation, unknown mode error |
| `test_stats.py` | `SessionStats` | Counts, score percentage, division by zero, reset, validation |
| `test_ui.py` | `QuizSession` | Correct/incorrect/skip/exit flows, empty deck, keyboard interrupt |
| `test_main.py` | `main()` | Full CLI integration, bad file, bad mode, stats flag |
| `test_task_manager.py` | `TaskManager` | CRUD, priority, completion timestamp |

Test coverage is above 80 percent for all application modules. The adaptive
mode has dedicated termination tests that guarantee the session ends under all
realistic answer patterns.

---

## Design Patterns

### Strategy Pattern

`QuizMode` is an abstract base class in `utils/quiz_engine.py` that defines
a four-method interface: `start`, `next_card`, `record_answer`, and
`is_complete`. `SequentialMode`, `RandomMode`, and `AdaptiveMode` each
implement this interface with a different ordering algorithm. `QuizSession` in
`utils/ui.py` holds a reference to a `QuizMode` instance and delegates all
card-ordering decisions to it, making the session code independent of which
algorithm is active.

This pattern was chosen because the three algorithms share the same interface
but differ completely in their internal state. Without Strategy, the session
would contain a conditional block for every mode, making it harder to test each
algorithm in isolation and impossible to add a new mode without modifying the
session class.

### Factory Pattern

`QuizModeFactory` in `utils/quiz_engine.py` maps mode-name strings to concrete
`QuizMode` classes via a `_MODES` dictionary. Its `create()` static method
normalises the input string, looks up the class, raises a descriptive
`ValueError` on unknown names, and returns a new instance. `main.py` imports
only `QuizModeFactory` and has no direct dependency on any concrete mode class.

This pattern was chosen to centralise object-creation logic and input
validation. Callers do not need to know which class to instantiate or how to
handle invalid mode names.

Full Udacity Design Patterns Template documentation is in
`docs/design_patterns.md`.

---

## Technical Challenges and Solutions

### Challenge 1: AdaptiveMode Termination Guarantee

**Problem:** The adaptive mode must guarantee termination even when users
answer incorrectly many times. An implementation that simply re-enqueues
failed cards with no boundary check can loop indefinitely.

**Solution:** The retry pass mechanism tracks the size of the retry queue at
the start of each pass (`_current_retry_pass_size`). Cards re-enqueued during
a pass are deferred to the next pass; the current pass size is never mutated
after it is set. This guarantees that every pass has a fixed, finite number of
cards, and the session terminates as long as the user eventually answers each
card correctly.

**AI Involvement:** The initial AI implementation had the bug described above.
The student identified it by writing a termination test and observing an
infinite loop. The corrected design was proposed by the student and confirmed
by Claude.

### Challenge 2: Dual JSON Format Support

**Problem:** Flashcard files found in the wild use two common formats: a bare
array and a wrapped object with a `"cards"` key. The loader needed to support
both without requiring users to convert their files.

**Solution:** `FileHandler.load_flashcards` inspects the parsed JSON type. If
it is a `list`, it is used directly. If it is a `dict` with a `"cards"` key,
the list is extracted. Any other structure raises a descriptive `ValueError`.

**AI Involvement:** Claude proposed this detection approach on the first pass.
No modification was required.

### Challenge 3: Testing Random Mode Deterministically

**Problem:** `RandomMode` shuffles cards randomly, making test assertions on
ordering non-deterministic by default.

**Solution:** `RandomMode.__init__` accepts an optional `seed` parameter that
is passed to `random.Random(seed)`. Tests construct `RandomMode(seed=42)` to
get a deterministic shuffle, then assert the specific order produced by that
seed. Production code passes no seed, preserving true randomness.

**AI Involvement:** Claude identified this risk during the architecture review
and proposed the seed parameter. The student accepted the design.

---

## Learning Outcomes

### Technical Skills Developed

- Implementing the Strategy and Factory patterns in a real project, not just
  as textbook examples
- Dependency injection as a testability technique in Python
- Writing mypy-compatible code with abstract base classes and generic types
- Using `deque` for efficient front-removal in queue-based algorithms
- Organising a test suite by module with setup/teardown fixtures

### AI Collaboration Skills

- Starting every session with a read-and-summarise step before writing any
  code produces better architecture proposals
- Requiring the AI to state intended file changes before making them prevents
  scope creep
- Running linting and testing tools immediately after implementation catches
  issues while context is fresh
- AI-generated test assumptions must be reviewed for logical consistency, not
  just syntax
- Asking the AI to justify design decisions (why one file vs. two, why
  `@staticmethod` vs. instance method) produces more reasoned and defensible
  choices

### Software Engineering Insights

The most significant insight from this project is that AI-assisted development
is most effective when the human establishes clear contracts and boundaries
before authorising implementation. Every module in this project was specified
(interface, error handling contract, test cases) before Claude wrote a single
line of code. The result is that almost no logic changes were required after
implementation — the only corrections were to an algorithm bug that a test
exposed and to test assumptions that were logically impossible. This is a
substantially better outcome than starting with generated code and trying to
refactor it into a good design after the fact.

---

## Reflection

### What Worked Well

The phased approach — inspect, specify, implement, verify — produced reliable
results. Each phase delivered working, tested, linted code before the next
phase began, so there was no accumulated technical debt. The dependency
injection design in `QuizSession` was particularly effective: it made the UI
layer fully testable without any monkeypatching or subprocess calls.

### What Could Be Improved

The adaptive mode's retry algorithm, while correct, is more complex than
necessary for a learning project. A simpler model — two fixed passes over
missed cards — would be easier to reason about and test. The complexity was
worth accepting because the current design handles edge cases (cards missed
multiple times) more gracefully, but the trade-off should be revisited if the
codebase grows.

### Future Enhancements

- Spaced repetition mode (SM-2 algorithm) as a fourth `QuizMode` strategy,
  demonstrating that the Strategy pattern makes the extension trivial
- Persistent progress tracking across sessions using `FileHandler`
- A `--reverse` flag to quiz from the back side of each card
- Batch statistics export to JSON for progress visualisation

---

## Conclusion

The Flashcard Quizzer project demonstrated that AI-assisted development can
produce high-quality, well-structured Python code when the human developer
maintains clear ownership of architecture, contracts, and quality gates.
Claude accelerated implementation significantly — modules that would have taken
hours to write were produced in minutes — but every non-trivial deliverable
required human review to catch algorithm bugs, fix test assumptions, and enforce
design decisions.

The most durable lesson is that the value of an AI assistant is proportional
to the quality of the specification the developer provides. Vague prompts
produced over-engineered architectures and optimistic test assumptions. Precise
prompts with explicit contracts and constraints produced correct, lean
implementations that needed minimal correction. This pattern will directly
influence how I approach AI collaboration in future projects.

---

## Appendices

### Appendix A: AI Interaction Log

Full interaction records, including prompts, AI responses, changes made, and
lessons learned, are in `docs/ai_edit_log.md`. Key entries: Phase 1 Data Layer
(2026-08-24), Phase 2 Quiz Engine (2026-08-24), Phase 3 SessionStats
(2026-08-24), Phase 4 UI Layer, Phase 5 CLI Entry Point.

### Appendix B: Code Statistics

- **Source files:** 6 application modules + `main.py`
- **Test files:** 7 test modules
- **Total tests:** 156 passing, 0 failing
- **Flake8 violations:** 0
- **mypy errors:** 0 (with `--check-untyped-defs`)
- **Black compliance:** all files formatted at 79-character line length

### Appendix C: Resources

- Python `abc` module documentation — abstract base classes
- Gang of Four: *Design Patterns: Elements of Reusable Object-Oriented Software*
- pytest documentation — fixtures, parametrize, monkeypatch
- mypy documentation — type checking with abstract base classes
- Black documentation — code formatting with line-length configuration
