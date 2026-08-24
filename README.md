# Flashcard Quizzer

An interactive command-line flashcard quiz tool written in Python. Load any
JSON flashcard file, choose a quiz mode, and study interactively with coloured
feedback and session statistics.

---

## Features

- **Three quiz modes**
  - `sequential` — presents every card once in the original file order
  - `random` — shuffles the deck before each session
  - `adaptive` — re-queues missed cards until all are answered correctly
- **Dual JSON format support** — bare array `[{...}]` or wrapped
  `{"cards": [{...}]}`
- **Session statistics** — correct, incorrect, and skipped counts with a score
  percentage printed at the end when `--stats` is passed
- **Coloured terminal feedback** — green for correct answers, red for incorrect
- **Skip and exit commands** — type `skip` to skip a card or `exit` to quit
  mid-session
- **Descriptive error messages** — clear output for missing files, malformed
  JSON, and unrecognised mode names
- **Fully typed codebase** — passes mypy with `--check-untyped-defs` and
  Flake8 at 79-character line length

---

## Dependencies

### Runtime

| Package | Version | Purpose |
|---|---|---|
| `colorama` | ≥ 0.4.6 | Cross-platform ANSI colour output |

### Development / Testing

| Package | Version | Purpose |
|---|---|---|
| `pytest` | ≥ 7.0.0 | Test runner |
| `pytest-cov` | ≥ 4.0.0 | Coverage reporting |
| `black` | ≥ 22.0.0 | Code formatter |
| `flake8` | ≥ 5.0.0 | Linter |
| `isort` | ≥ 5.10.0 | Import sorter |
| `mypy` | ≥ 1.0.0 | Static type checker |

---

## Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd flashcard-quizzer

# 2. Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## JSON Flashcard Format

Two formats are supported.

**Flat list** (simplest):

```json
[
  {"front": "What is the capital of France?", "back": "Paris"},
  {"front": "What does CPU stand for?",       "back": "Central Processing Unit"},
  {"front": "What is 2 + 2?",                 "back": "4"}
]
```

**Wrapped object**:

```json
{
  "cards": [
    {"front": "What is the capital of France?", "back": "Paris"},
    {"front": "What does CPU stand for?",       "back": "Central Processing Unit"}
  ]
}
```

Every card must have a non-empty `"front"` (question) and `"back"` (answer).
Extra fields are ignored.

---

## CLI Arguments

```
usage: python main.py -f FILE [-m MODE] [--stats]

required arguments:
  -f FILE, --file FILE    Path to a JSON flashcard file

optional arguments:
  -m MODE, --mode MODE    Quiz mode: sequential, random, or adaptive
                          (default: sequential)
  --stats                 Print session statistics after the quiz
  -h, --help              Show this help message and exit
```

---

## Usage Examples

**Sequential quiz (default mode):**

```bash
python main.py -f data/sample_cards.json
```

**Random mode:**

```bash
python main.py -f data/sample_cards.json -m random
```

**Adaptive mode with statistics:**

```bash
python main.py -f data/sample_cards.json -m adaptive --stats
```

**Wrapped JSON format:**

```bash
python main.py -f data/wrapped_cards.json -m sequential --stats
```

**Sample session output:**

```
Quiz started. Type 'exit' to quit or 'skip' to skip a card.

Question: What is the capital of France?
Your answer (or 'skip' / 'exit'): paris
Correct!

Question: What does CPU stand for?
Your answer (or 'skip' / 'exit'): skip
Skipped.

Question: What is 2 + 2?
Your answer (or 'skip' / 'exit'): 5
Incorrect. The correct answer is: 4

Session complete.
Correct: 1 | Incorrect: 1 | Skipped: 1 | Score: 50.0%
```

---

## Project Structure

```
flashcard-quizzer/
├── main.py                       # CLI entry point (argparse + orchestration)
├── requirements.txt
├── data/
│   ├── sample_cards.json         # Example flat-list flashcard file
│   └── wrapped_cards.json        # Example wrapped-object flashcard file
├── utils/
│   ├── __init__.py
│   ├── flashcard.py              # Flashcard dataclass + validation
│   ├── file_handler.py           # JSON loading (FileHandler.load_flashcards)
│   ├── quiz_engine.py            # QuizMode ABC, 3 strategies, QuizModeFactory
│   ├── stats.py                  # SessionStats (correct/incorrect/skipped)
│   ├── task_manager.py           # Starter demo code (not used by quiz app)
│   └── ui.py                     # QuizSession — terminal I/O + session loop
├── tests/
│   ├── __init__.py
│   ├── test_flashcard_loader.py  # FileHandler.load_flashcards (27 tests)
│   ├── test_file_handler.py      # FileHandler CRUD operations
│   ├── test_quiz_modes.py        # All three modes + factory (27 tests)
│   ├── test_stats.py             # SessionStats
│   ├── test_ui.py                # QuizSession interaction flows
│   ├── test_main.py              # CLI integration tests
│   └── test_task_manager.py      # TaskManager (starter demo)
├── docs/
│   ├── ai_edit_log.md            # Full AI interaction log
│   ├── design_patterns.md        # Udacity Design Patterns documentation
│   └── report_template.md        # Completed final project report
├── ai_guidance/
│   ├── prompting_best_practices.md
│   └── code_review_checklist.md
└── prompts/                      # Saved prompt files for each dev phase
```

---

## Design Patterns

### Strategy Pattern

`QuizMode` (`utils/quiz_engine.py`) is an abstract base class with a common
interface: `start()`, `next_card()`, `record_answer()`, `is_complete()`.
`SequentialMode`, `RandomMode`, and `AdaptiveMode` each implement this
interface. `QuizSession` in `utils/ui.py` holds any `QuizMode` and delegates
card ordering to it, so the session logic never changes when a new mode is
added.

### Factory Pattern

`QuizModeFactory.create(mode)` (`utils/quiz_engine.py`) maps mode-name strings
to concrete classes, normalises the input, and raises a descriptive
`ValueError` for unrecognised names. `main.py` imports only the factory; it
has no direct dependency on any concrete mode class.

---

## Testing

```bash
# Run all 156 tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run a specific test file verbosely
pytest tests/test_quiz_modes.py -v

# Run all quality checks
black . --line-length 79 --check
isort . --check-only
flake8 . --max-line-length 79
mypy main.py utils/ --check-untyped-defs --ignore-missing-imports
pytest
```

---

## Code Quality

All source files comply with:

- **Black** formatting at 79-character line length
- **Flake8** linting — 0 violations
- **mypy** type checking with `--check-untyped-defs` — 0 errors
- **isort** import ordering

---

## AI Collaboration

This project was built with Claude as an AI coding assistant. All interactions
are documented in `docs/ai_edit_log.md`. The development followed a phased
workflow: inspect existing code → specify requirements → implement → run
quality checks → review before accepting. See `docs/report_template.md` for
the full project report describing the collaboration process.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

### 🛠️ Development Tools

#### Code Quality Tools

- **Black**: Code formatter
  ```bash
  black .
  ```

- **isort**: Import organizer
  ```bash
  isort .
  ```

- **flake8**: Linting
  ```bash
  flake8 .
  ```

- **mypy**: Type checking
  ```bash
  mypy .
  ```

- **pytest**: Testing framework
  ```bash
  pytest --cov=. --cov-report=html
  ```

#### Pre-commit Hooks (Optional)

Set up pre-commit hooks for automatic code quality checks:

```bash
pre-commit install
```

## Testing

The project includes comprehensive unit tests demonstrating proper testing practices for AI-assisted development.

### Tests Break Down

**TaskManager Tests (`test_task_manager.py`):**
- `test_add_task_returns_id()` - Verifies task creation returns valid ID
- `test_get_task_by_id()` - Tests task retrieval with proper data structure
- `test_complete_task()` - Validates task completion with timestamps
- `test_delete_task()` - Ensures proper task deletion and error handling
- `test_get_nonexistent_task_raises_error()` - Tests error handling for invalid IDs

**FileHandler Tests (`test_file_handler.py`):**
- `test_save_data_creates_file()` - Verifies JSON file creation and content
- `test_load_nonexistent_file_returns_empty_dict()` - Tests graceful error handling
- `test_file_exists()` - Validates file existence checking
- `test_delete_file()` - Tests file cleanup functionality
- `test_list_files()` - Verifies directory listing capabilities

```bash
# Run all tests
pytest

# Run with coverage report (aim for >80% coverage)
pytest --cov=. --cov-report=html

# Run specific test file with verbose output
pytest tests/test_task_manager.py -v

# Run all quality checks
black . && isort . && flake8 . && mypy . && pytest
```

## Project Instructions

This section contains all the student deliverables for this project.

### Learning Objectives
- **AI Collaboration**: Learn to effectively work with AI assistants to generate, review, and refactor code while maintaining code quality
- **Software Engineering**: Apply design patterns, separation of concerns, and modular architecture
- **Test-Driven Development**: Write and maintain comprehensive unit tests with good coverage
- **Code Quality**: Use linting, formatting, and type checking tools for professional-grade code
- **Documentation**: Document AI interactions and development decisions throughout the process

### AI-Assisted Development Workflow

#### 1. Planning Phase
- Use AI to help break down requirements into smaller, manageable tasks
- Ask for architectural suggestions and design pattern recommendations
- Review the `/ai_guidance/prompting_best_practices.md` for effective prompting techniques
- Use the provided slash commands in `/.claude/commands/` for common tasks

#### 2. Implementation Phase
- Generate initial code with AI assistance using specific, contextual prompts
- Always review and understand AI-generated code before accepting it
- Test AI-generated code thoroughly with various inputs and edge cases
- Refactor for clarity, maintainability, and adherence to project standards

#### 3. Review Phase
- Use AI to help identify potential issues or improvements
- Follow the `/ai_guidance/code_review_checklist.md` for systematic code review
- Ask for code review suggestions and alternative implementations
- Validate that the code follows project conventions and security best practices

#### 4. Documentation Phase
- Document your AI interactions in `/docs/ai_edit_log.md` with specific examples
- Explain your decisions and modifications to AI suggestions
- Complete the final report using `/docs/report_template.md`
- Update this README with new features and learnings

### Assessment Criteria

Your project will be evaluated on:

1. **Functionality**: Does the application work as intended with proper error handling?
2. **Code Quality**: Is the code well-structured, readable, and maintainable?
3. **Testing**: Are there comprehensive unit tests with good coverage (>80%)?
4. **AI Collaboration**: Did you effectively use AI assistance while maintaining code quality?
5. **Documentation**: Are your AI interactions and decisions well-documented?

### Example AI Prompts

- "Help me implement a priority queue for tasks using the strategy pattern"
- "Review this code for potential security vulnerabilities"
- "Suggest improvements to make this code more maintainable"
- "Help me write comprehensive unit tests for this function"

### AI Guidance Resources

- `/ai_guidance/prompting_best_practices.md` - Learn effective AI prompting techniques
- `/ai_guidance/code_review_checklist.md` - Systematic approach to reviewing AI-generated code
- `/.claude/commands/generate-function` - Generate well-structured Python functions
- `/.claude/commands/review-code` - Get comprehensive code reviews
- `/.claude/commands/debug-help` - Debug issues with AI assistance
- `/.claude/commands/refactor-code` - Refactor code with design patterns
- `/docs/design_patterns.md` - Examples of implementing design patterns with AI assistance

### Project Structure

```
starter/
├── main.py                 # Main application entry point
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── task_manager.py     # Task management functionality
│   └── file_handler.py     # File I/O operations
├── tests/                  # Unit test suite
│   ├── __init__.py
│   ├── test_task_manager.py
│   └── test_file_handler.py
├── docs/                   # Documentation and templates
│   ├── ai_edit_log.md      # AI interaction tracking
│   ├── design_patterns.md  # Design pattern examples
│   └── report_template.md  # Final report template
├── ai_guidance/            # AI prompting best practices
│   ├── prompting_best_practices.md
│   └── code_review_checklist.md
├── .claude/                # Claude-specific configuration
│   ├── CLAUDE.md           # Claude configuration
│   ├── commands/           # Slash commands
│   └── mcp.json           # MCP configuration
├── requirements.txt        # Python dependencies
├── .editorconfig          # Code formatting rules
└── README.md              # This file
```

## Built With

* [Python](https://www.python.org/) - Core programming language
* [pytest](https://docs.pytest.org/) - Testing framework for comprehensive unit tests
* [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage reporting for tests
* [Black](https://black.readthedocs.io/) - Code formatter for consistent style
* [isort](https://pycqa.github.io/isort/) - Import organizer for clean code structure
* [flake8](https://flake8.pycqa.org/) - Linting tool for code quality
* [mypy](https://mypy.readthedocs.io/) - Static type checker for better code reliability
* [pre-commit](https://pre-commit.com/) - Git hook framework for automated quality checks
* [Claude](https://claude.ai/) - AI assistant for code generation and review

## License

[License](LICENSE.txt)

---

**Remember**: The goal is not just to build a working application, but to learn how to effectively collaborate with AI while maintaining high software engineering standards. Take time to understand the code, ask questions, and document your learning journey!
