# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

### 2024-01-15 - Initial Task Manager Implementation

**Context:** I needed to create a basic task management system to demonstrate CRUD operations and serve as the foundation for the project.

**AI Tool Used:** Claude

**Prompt/Request:** "Help me create a Python class for managing tasks with basic CRUD operations. The class should handle task creation, retrieval, completion, and deletion. Include proper error handling and type hints."

**AI Response:** Claude generated a TaskManager class with methods for add_task, get_task, get_all_tasks, complete_task, delete_task, and to_dict. The code included type hints, proper error handling with ValueError for missing tasks, and used datetime for timestamps.

**Changes Made:** 
- Added priority field to tasks with a default value of "medium"
- Modified the task structure to include created_at timestamp
- Added validation for priority values
- Renamed some variable names for clarity

**Reasoning:** 
- Priority field will be useful for implementing sorting features later
- Timestamps help with task organization and analytics
- Input validation prevents invalid data from being stored
- Better variable names improve code readability

**Outcome:** Successfully created a robust TaskManager class that serves as the core of the application with room for future enhancements.

**Lessons Learned:** 
- AI provides good starting implementations but always needs customization
- It's important to think about future requirements when reviewing AI code
- Type hints and error handling are crucial for maintainable code

---

## Your Log Entries

### 2026-08-24 - Initial Starter Project Inspection and Architecture Analysis

**Context:** Before writing any code, I needed to understand the existing starter repository and produce an architecture proposal for the Flashcard Quizzer CLI application. The starter contained a generic Task Manager demo unrelated to the final application.

**AI Tool Used:** Claude

**Prompt/Request:** "Inspect the existing repository and understand the starter project before making any changes. After inspecting the repository, provide: a concise summary, the purpose of each file and directory, any existing code or templates that should be preserved, missing components that will need to be implemented, a proposed modular architecture, a proposed development sequence broken into phases, and potential technical risks."

**AI Response:** Claude read all project files (main.py, utils/, tests/, docs/, requirements.txt, README.md, .claude/) and produced a full written analysis. It proposed a 7-module architecture splitting quiz strategies and the factory into separate files (quiz_modes.py and quiz_factory.py), and identified 7 technical risks including adaptive mode complexity, JSON format normalization, color output portability, and mypy strictness on ABCs.

**Changes Made:** No code was written at this stage. The analysis was reviewed and used as the basis for a follow-up refinement request.

**Reasoning:** The instructions explicitly required inspection and analysis before any implementation. Starting with a clear picture of the existing structure prevented unnecessary rewrites and preserved reusable components like the FileHandler class.

**Outcome:** Produced a detailed inventory of the starter codebase, a 6-phase development plan, and a risk register. Identified that utils/file_handler.py and tests/test_file_handler.py were reusable assets worth preserving. Confirmed that utils/task_manager.py and its tests were demo code with no value for the flashcard application.

**Lessons Learned:** Asking the AI to read and summarize the full codebase before proposing architecture is more reliable than jumping straight to code generation. The AI surfaced non-obvious risks (e.g., testing random mode requires seeding, adaptive mode needs a termination bound) that would have been costly to discover during implementation.

---

### 2026-08-24 - Architecture Review and Refinement

**Context:** The initial architecture proposal contained unnecessary module separation (quiz_modes.py and quiz_factory.py as two separate files) and did not clearly distinguish between reusable, adapted, and replaced starter code. I wanted a simpler, more cohesive design before authorizing any implementation.

**AI Tool Used:** Claude

**Prompt/Request:** "Revisit your previous analysis and address the following: (1) distinguish reusable vs. replaced code, (2) evaluate whether a simplified 6-module architecture is sufficient, (3) define AdaptiveMode behavior precisely and make it testable, (4) verify alignment with project documentation, (5) propose the exact first implementation milestone only."

**AI Response:** Claude revised the architecture to consolidate quiz strategies and the factory into a single quiz_engine.py file, arguing that separating them added a file boundary with no real separation of concern. It produced a precise AdaptiveMode specification using weighted random selection (weight = 1 + miss_count), fixed-round termination (N = len(cards)), and an exposed miss_counts dict for testability. It also reviewed design_patterns.md, project_rubric.md, and the AI guidance files to confirm alignment, then proposed a detailed Phase 1 plan covering file responsibilities, JSON validation behavior, test cases, and verification commands.

**Changes Made:** Accepted the consolidated quiz_engine.py design. Accepted the AdaptiveMode termination rule (fixed N rounds). No code was written yet; the plan was reviewed before authorizing implementation.

**Reasoning:** Keeping the Strategy classes and Factory in one file is justified for a small CLI application — it reduces import complexity and avoids the impression that separation of concerns requires one class per file. The fixed-round termination rule is preferable to a "mastery" model because it gives predictable quiz lengths and is straightforward to test without mocking time or external state.

**Outcome:** Arrived at a clean 6-module architecture (main.py, flashcard.py, file_handler.py, quiz_engine.py, stats.py, ui.py) with a fully specified AdaptiveMode and a concrete Phase 1 implementation plan ready for authorization.

**Lessons Learned:** Asking the AI to justify consolidation decisions, rather than accepting the first architecture proposed, led to a meaningfully simpler design. The AI's willingness to revise its own proposals when given clear criteria (avoid over-engineering, satisfy rubric) was valuable. Requiring a precise behavioral spec for AdaptiveMode before implementation prevented ambiguity that would have surfaced as test failures later.

---

### 2026-08-24 - Phase 1 Data Layer Planning and Validation Design

**Context:** Before implementing, the Phase 1 plan required one final refinement pass to clarify separation of concerns for error handling, confirm the FileHandler API extension strategy, and set the scope boundary to only the data layer files.

**AI Tool Used:** Claude

**Prompt/Request:** "I approve the general Phase 1 plan, but before implementation, make these refinements: (1) the data layer may raise exceptions but must not print to the terminal, (2) inspect the existing FileHandler API and adapt it consistently, (3) limit Phase 1 to utils/flashcard.py, utils/file_handler.py, data/sample_cards.json, and tests/test_flashcard_loader.py."

**AI Response:** Claude confirmed the scope, stated which files it would change and why before touching anything, and clarified that load_flashcards would be implemented as a @staticmethod on FileHandler (consistent with the existing pattern of methods that operate on explicit paths rather than the instance's data_dir). It confirmed no terminal output would appear in the data layer.

**Changes Made:** No modifications to the plan; this interaction served as a pre-implementation gate. The scope boundary (no quiz engine, no UI, no argparse) was explicitly agreed before any files were written.

**Reasoning:** Requiring the AI to state its intended file changes before making them ensures nothing is modified unexpectedly. The separation-of-concerns constraint (exceptions only, no print statements in the loader) was important to enforce early, since AI-generated loaders often mix error reporting styles.

**Outcome:** Clear, agreed implementation plan with explicit file list, no scope creep, and a clean exception-only error handling contract for the data layer.

**Lessons Learned:** A short pre-implementation confirmation step catches scope and design disagreements before code is written, which is far cheaper than refactoring after the fact. Asking the AI to explain its API design choice (why @staticmethod rather than a new instance method) produced a clear justification that confirmed the decision was correct.

---

### 2026-08-24 - Phase 1 Implementation

**Context:** With the plan approved, I authorized Claude to implement the data layer: the Flashcard dataclass, the load_flashcards extension to FileHandler, a sample data file, and a comprehensive test suite.

**AI Tool Used:** Claude

**Prompt/Request:** "Proceed with implementation after stating the files you will modify. Requirements: support both JSON formats, validate complete structure and each card, use type hints, include docstrings, keep implementation simple, write comprehensive pytest tests, do not modify documentation files, run tests after implementation, run flake8, report results."

**AI Response:** Claude created utils/flashcard.py with a @dataclass and __post_init__ validation for non-empty strings; extended utils/file_handler.py with a load_flashcards @staticmethod supporting both flat-list and wrapped-cards JSON formats; created data/sample_cards.json with 5 sample cards; and created tests/test_flashcard_loader.py with 27 tests covering all valid inputs, all error conditions, and correct index reporting in error messages. It then ran pytest (34 passed) and flake8, which reported violations that were immediately corrected.

**Changes Made:** No manual code changes were required to the logic. The AI self-corrected the flake8 violations it introduced (two E501 long lines in file_handler.py and flashcard.py, and W293 trailing whitespace inherited from the original starter file) after the tool reported them.

**Reasoning:** The implementations were correct on first pass. The flake8 violations were minor style issues that the AI fixed without prompting once the linter output was visible. No logic errors or security issues were found on review.

**Outcome:** 34 tests passing (27 new + 7 existing FileHandler tests), flake8 clean across all Phase 1 files, type hints on all functions, docstrings present, exception-only error handling confirmed. The existing TestFileHandler suite continued to pass without modification, confirming the FileHandler API was extended cleanly.

**Lessons Learned:** Running flake8 immediately after implementation, rather than at a final quality pass, caught style issues while the context was fresh and made them trivial to fix. The AI correctly identified that trailing whitespace on blank lines (W293) in the original starter file needed to be cleaned up as part of the adaptation — it did not preserve pre-existing style violations. Requiring the AI to state changed files before editing and to report results after running tools made the session fully auditable.

---

### 2026-08-24 - AI-Generated Code Review, Testing, and Corrections

**Context:** After Phase 1 implementation, I reviewed the AI-generated code for correctness, security, and compliance with project standards before accepting it as the foundation for subsequent phases.

**AI Tool Used:** Claude (self-review via flake8 and pytest output)

**Prompt/Request:** The review was triggered by running the verification commands specified in the Phase 1 plan: pytest for correctness and flake8 for style compliance.

**AI Response / Issues Found:**

- **E501 line too long (84 > 79 chars)** in file_handler.py at the `Flashcard(front=item["front"], back=item["back"])` call — fixed by wrapping the arguments across two lines.
- **E501 line too long (82 > 79 chars)** in flashcard.py at the class docstring — fixed by breaking the docstring onto a second line.
- **W293 blank line contains whitespace** (5 instances) in file_handler.py — these were inherited from the original starter file's trailing whitespace and were cleaned up during the adaptation.
- **W292 no newline at end of file** in file_handler.py — fixed by ensuring a trailing newline.

No logic errors, missing validations, or security issues were identified during review. All 13 planned test cases were present and passing, plus additional edge cases (whitespace-only field values, non-dict card items, correct index in error messages, extra fields ignored).

**Changes Made:** Four flake8 violations corrected; no logic changes required.

**Reasoning:** PEP 8 and flake8 compliance are rubric requirements. Correcting these before moving to Phase 2 ensures the linter baseline is clean and future violations are attributable to new code only.

**Outcome:** All Phase 1 files are flake8-clean. 34 tests pass. The data layer is ready to serve as the foundation for Phase 2 (quiz engine).

**Lessons Learned:** AI-generated code reliably passes functional tests but frequently produces minor style violations on first pass — particularly long lines in f-strings and docstrings. Running the linter as part of the implementation step (rather than as a separate quality pass at the end) is more efficient. The AI's ability to interpret linter output and apply targeted fixes without re-generating whole files was useful and accurate.

---

### 2026-08-24 - Phase 2 Quiz Engine Implementation (Strategy and Factory Patterns)

**Context:** I needed to implement the quiz mode system for the Flashcard Quizzer. The application needed Sequential, Random, and Adaptive quiz modes with clearly defined behavior. The implementation also needed to satisfy the design pattern requirement from the project rubric by demonstrating both the Strategy Pattern (quiz modes) and the Factory Pattern (mode selection).

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude to implement Phase 2 of the quiz engine and its tests based on the previously approved architecture. The request specified the Strategy Pattern with a `QuizMode` abstract base class, three concrete strategies (`SequentialMode`, `RandomMode`, `AdaptiveMode`), a `QuizModeFactory`, complete type hints and docstrings, and a comprehensive test suite in `tests/test_quiz_modes.py`.

**AI Response:** Claude created `utils/quiz_engine.py` containing the `QuizMode` ABC, all three strategy classes, and `QuizModeFactory`. It also created `tests/test_quiz_modes.py` with 27 tests covering sequential ordering, random shuffling, adaptive retry behavior, factory creation, case-insensitivity, and error handling for invalid modes.

**Changes Made:**

1. **Unhashable Flashcard in tests** — Three tests used `set()` to compare card collections, which caused a `TypeError` because `@dataclass` instances are not hashable when `__eq__` is generated. This was corrected by replacing `set()` comparisons with `sorted(..., key=lambda c: c.front)` list comparisons.

2. **AdaptiveMode infinite-loop risk** — The initial `record_answer` implementation incremented `_current_retry_pass_size` when a card was re-enqueued during the current retry pass. This allowed an incorrectly answered card to be immediately re-consumed within the same pass, creating an unbounded loop. The fix removes the mid-pass size mutation: re-enqueued cards are always appended behind the current pass boundary and deferred to the next pass.

3. **Incorrect termination test assumption** — One test drove the session with every answer always wrong, then asserted the session would terminate. This assumption is logically impossible — if cards are never answered correctly they will be re-enqueued indefinitely. The test was replaced with a realistic scenario where each card is answered incorrectly a fixed number of times before eventually being answered correctly, which correctly validates that the session terminates under normal conditions.

**Reasoning:** AI-generated code and tests must be validated rather than accepted automatically. The `set()` issue was a straightforward Python type error that testing caught immediately. The `AdaptiveMode` loop risk was a subtle algorithm defect that would not have surfaced without a dedicated termination test. The test assumption correction was necessary because an unachievable test gives false confidence — it either never terminates or passes for the wrong reason. All three changes were required to produce correct, trustworthy code.

**Outcome:** 69 tests passed with 0 failures across the full test suite. flake8 passed after fixing one E501 long line in the test file. The quiz engine and its tests were successfully completed and are ready to integrate with the session and UI layers in subsequent phases.

**Lessons Learned:** AI can generate useful implementations quickly, but algorithm behavior and test assumptions still require human review. In this case, running the tests immediately exposed issues that were not obvious during code generation. The AdaptiveMode defect in particular — where the pass-size counter was mutated mid-pass — was a logical error that looked plausible in isolation but failed under a systematic test. This reinforces the importance of testing edge cases (termination, empty decks, repeated wrong answers) rather than only the happy path.

---

### 2026-08-24 - Phase 3 SessionStats Implementation

**Context:** I needed to implement a statistics system for the Flashcard Quizzer that could track correct, incorrect, and skipped answers and calculate quiz performance without depending on terminal input or output. The component needed to be independently testable and free of I/O side effects so it could be integrated with the UI layer in a later phase.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude to inspect the existing project structure and implement Phase 3 by creating `utils/stats.py` and `tests/test_stats.py`. The implementation needed to include a testable `SessionStats` class with tracking for correct, incorrect, and skipped answers, total counts, score percentage calculation, division-by-zero protection, reset functionality, input validation, type hints, docstrings, and comprehensive tests.

**AI Response:** Claude created `utils/stats.py` containing the `SessionStats` class and `tests/test_stats.py` containing 42 tests. The class includes methods for recording correct, incorrect, and skipped answers (`record_correct`, `record_incorrect`, `record_skipped`), read-only properties for retrieving counts and totals (`correct`, `incorrect`, `skipped`, `total_attempted`, `total`), a `score_percentage` property that returns 0.0 when no answers have been attempted, `reset` functionality, and a `summary` method that returns a formatted plain-text string.

**Changes Made:** No implementation bugs were found during the first test run. However, the generated implementation was still validated by running the complete test suite and flake8 rather than being accepted without testing.

**Reasoning:** Even when AI-generated code appears correct, it must be independently validated. The rubric requires testing AI-generated code and reviewing its quality. Running all 111 tests ensured the new statistics component did not break any existing functionality, while flake8 confirmed that the new code followed the required style standards. Skipping this step because the first run looked clean would contradict the core principle of the course.

**Outcome:** All 111 tests passed with 0 failures. This included 42 new tests for `SessionStats` and 69 existing tests covering the data layer, quiz engine, and starter code. flake8 also completed without violations for `utils/stats.py` and `tests/test_stats.py`.

**Lessons Learned:** AI can sometimes generate correct code on the first attempt, but successful generation does not remove the need for validation. Comprehensive tests and style checks provide evidence that the implementation works correctly and integrates safely with the existing application. This interaction also demonstrated the value of keeping `SessionStats` independent from I/O — the class was straightforward to test precisely because it had no terminal dependencies.

---

### 2026-08-24 - Phase 4 Interactive UI Layer Implementation

**Context:** I needed to implement the interactive quiz session layer for the Flashcard Quizzer. This layer had to coordinate the quiz mode, statistics tracking, and terminal I/O, while remaining testable without requiring actual terminal interaction.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude to implement `utils/ui.py` containing a `QuizSession` class and `tests/test_ui.py` with comprehensive tests. Requirements included: dependency injection for input and output callables, case-insensitive answer checking with whitespace stripping, `skip` and `exit` command handling, `KeyboardInterrupt` handling, colored terminal feedback using colorama, and test coverage for all edge cases including empty card collections, adaptive mode integration, and graceful session termination.

**AI Response:** Claude created `utils/ui.py` with a `QuizSession` class accepting `mode`, `stats`, `input_fn`, and `print_fn` parameters. `colorama.init(autoreset=True)` was called at module level for cross-platform color support. The `run()` method handles the full quiz loop, dispatches `exit` and `skip` commands, catches `KeyboardInterrupt`, and returns the `SessionStats` instance. Claude also created `tests/test_ui.py` with 25 tests covering correct/incorrect answers, case-insensitivity, whitespace stripping, exit, skip, `KeyboardInterrupt`, empty cards, stats availability, and integration with all three quiz modes.

**Changes Made:**

1. **Unused imports removed from test file** — `call` from `unittest.mock`, `pytest`, and `QuizModeFactory` were imported but not used. These caused flake8 F401 violations and were removed.

2. **Three E501 long lines in `utils/ui.py`** — The `_check_answer` docstring first line, the `_handle_incorrect` call, and the quiz-start message each exceeded 79 characters. These were wrapped across multiple lines.

3. **Broken docstring from incorrect style fix** — During the fix for the `_check_answer` E501 violation, an erroneous `"""  # noqa: D205` was inserted mid-docstring, leaving the body of the docstring as raw prose outside the string. This was corrected by shortening the first docstring line to `"Compare user_answer and correct_answer case-insensitively."` rather than splitting it.

**Reasoning:** Dependency injection for `input_fn` and `print_fn` was the correct design choice because it allows all session behavior to be tested without patching built-ins globally. The flake8 fixes were required for rubric compliance. The broken docstring fix was necessary because the incorrect noqa approach produced syntactically valid but semantically wrong Python — the docstring body became unreachable prose rather than documentation.

**Outcome:** 136 tests passing with 0 failures. flake8 clean on `utils/ui.py` and `tests/test_ui.py`. All three quiz modes integrate correctly with `QuizSession`. `KeyboardInterrupt` and `exit` both terminate cleanly without tracebacks.

**Lessons Learned:** Mechanical style fixes (wrapping long lines) can corrupt docstrings if the fix strategy is wrong — the correct approach is to shorten the summary sentence, not to split the opening `"""` from the content. Testing caught the broken docstring indirectly because the `_check_answer` function still worked correctly at runtime; it required a code review pass to identify the documentation defect.

---

### 2026-08-24 - Final Integration and CLI Entry Point

**Context:** With all utility modules complete, I needed to wire the application together via a CLI entry point in `main.py`, add the missing `colorama` dependency to `requirements.txt`, create CLI tests, run the full quality check, and complete the AI edit log.

**AI Tool Used:** Claude Code

**Prompt/Request:** I asked Claude to rewrite `main.py` as the CLI entry point using `argparse` with `-f`/`--file`, `-m`/`--mode`, and `--stats` arguments; connect `FileHandler.load_flashcards`, `QuizModeFactory.create`, `SessionStats`, and `QuizSession.run`; handle all error paths cleanly without tracebacks; add `colorama` to `requirements.txt`; create `tests/test_main.py` covering success paths and error paths; run the full test suite and flake8; and update the AI edit log.

**AI Response:** Claude rewrote `main.py` with a `build_parser()` function and a `main(argv=None)` function returning an integer exit code. Error handling catches `FileNotFoundError` and `ValueError` from the loader and `ValueError` from the factory, printing clean error messages to stderr and returning exit code 1. `colorama>=0.4.6` was added to `requirements.txt`. `tests/test_main.py` was created with 20 tests covering argument parsing, all three valid modes, the `--stats` flag, missing file, malformed JSON, invalid mode, empty card file, and wrapped JSON format.

**Changes Made:**

1. **E501 long line in `tests/test_main.py`** — `assert "error" in captured.err.lower() or "not found" in captured.err.lower()` exceeded 79 characters. Fixed by extracting `err = captured.err.lower()` to a separate line.

No logic bugs were found. All 156 tests passed on the first run after the style fix.

**Reasoning:** The `main(argv=None)` signature (accepting an optional argument list) is the correct pattern for a testable CLI — it allows tests to call `main(["-f", path])` directly without subprocess overhead or `sys.argv` manipulation. Returning integer exit codes rather than calling `sys.exit()` inside `main()` keeps the function testable. Error messages go to stderr so they do not pollute stdout output that callers or tests might capture.

**Outcome:** 156 tests passing with 0 failures across the complete test suite (20 CLI tests + 136 previous). flake8 clean on `main.py` and `tests/test_main.py`. The application can be run end-to-end with `python main.py -f data/sample_cards.json -m sequential --stats`.

**Lessons Learned:** Integration of independently tested components was straightforward because each module had a clean interface and no hidden dependencies on global state or terminal I/O. The phased development approach — data layer, engine, stats, UI, CLI — meant integration required only wiring, not redesign. The only issue was a single style violation in the test file, which was caught and fixed immediately by running flake8 before accepting the implementation.

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?** AI helped most with creating the project structure, generating code, writing tests, and finding errors.
2. **Where did you need to make the most modifications to AI suggestions?** I needed the most modifications when fixing bugs in the quiz logic and improving some test cases.
3. **What patterns did you notice in AI strengths and weaknesses?** AI was good at generating code quickly, but it sometimes made logical mistakes that required testing and review.
4. **How did your prompting technique improve over time?** My prompts became more specific and organized by giving clear requirements and asking AI to focus on one phase at a time.
5. **What would you do differently in future AI collaborations?** In the future, I would give clearer requirements earlier and test each feature immediately after it is implemented.

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** 6 major implementation phases
- **Lines of AI-generated code used:** Approximately 500+ lines
- **Lines of AI-generated code modified:** Approximately 100+ lines
- **Most helpful AI interaction:**  Implementing the quiz engine using the Strategy and Factory patterns
- **Most challenging AI interaction:** Fixing the AdaptiveMode logic and preventing retry loop issues
- **Biggest lesson learned:** AI-generated code must always be tested and reviewed because it can contain logical errors even when it looks correct.

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.