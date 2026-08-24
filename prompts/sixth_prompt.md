Phase 4: Implement the interactive UI layer for the Flashcard Quizzer.

First inspect the current implementation before making changes, especially:

- utils/flashcard.py
- utils/file_handler.py
- utils/quiz_engine.py
- utils/stats.py
- all existing tests

Do not redesign or change the behavior of the existing quiz modes unless a change is required to integrate the UI correctly. Preserve the tested Strategy and Factory Pattern implementation.

Create:

- utils/ui.py
- tests/test_ui.py

The UI layer must be responsible for running an interactive quiz session while keeping the implementation testable.

Requirements:

1. Create a clear QuizSession or equivalent class responsible for coordinating:
   - quiz cards
   - a selected QuizMode
   - SessionStats
   - user input and output

2. The quiz session should:
   - display the front/question of each flashcard
   - collect the user's answer
   - compare answers case-insensitively
   - ignore leading and trailing whitespace when checking answers
   - display whether the answer is correct or incorrect
   - display the correct answer when the user is incorrect
   - notify the quiz mode whether the answer was correct or incorrect using the existing interface
   - update SessionStats appropriately

3. Support user commands:
   - "exit" should end the quiz gracefully
   - "skip" should skip the current card if this can be integrated cleanly with the existing quiz engine
   - Ctrl+C / KeyboardInterrupt should end the quiz gracefully without showing a traceback

4. Use colored terminal feedback if the project's dependencies and requirements support it:
   - green for correct answers
   - red for incorrect answers
   - initialize any color library correctly for cross-platform use

5. Keep the UI reasonably testable:
   - avoid tightly coupling all logic directly to builtins.input and print
   - use dependency injection, helper methods, or mocking where appropriate
   - do not add unnecessary complexity

6. Handle edge cases:
   - empty card collections
   - user exits before answering
   - skipped cards
   - KeyboardInterrupt
   - whitespace-only answers
   - repeated incorrect answers in AdaptiveMode
   - completion of Sequential and Random modes

7. Include complete type hints and appropriate docstrings.
8. Follow PEP 8 and the existing project style.
9. Do not modify docs/ai_edit_log.md during this phase.

Testing requirements:

Create comprehensive tests in tests/test_ui.py.

Test at minimum:

- correct answer updates statistics correctly
- incorrect answer updates statistics correctly
- answer comparison is case-insensitive
- answer comparison ignores surrounding whitespace
- exit command ends the session cleanly
- skip command behavior
- KeyboardInterrupt is handled gracefully
- SequentialMode integrates correctly
- RandomMode integrates correctly
- AdaptiveMode receives correct and incorrect answer results correctly
- empty card collection is handled appropriately
- final statistics are returned or available after the session

Use mocks or dependency injection for user input/output so tests do not require manual interaction.

Before completing:

1. Run the Phase 4 tests.
2. Run the complete pytest suite.
3. Fix all failures caused by the new implementation.
4. Run flake8 on the new and modified Phase 4 files.
5. If available and configured in the project, run formatting/type checks.
6. Do not modify docs/ai_edit_log.md.

At the end, provide a concise Phase 4 report containing:

- files created or modified
- implementation summary
- test results
- bugs or issues found during testing
- modifications made to AI-generated code
- remaining integration work

Implement the complete Phase 4 now rather than stopping after a design proposal.