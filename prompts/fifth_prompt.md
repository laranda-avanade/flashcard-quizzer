Phase 3: Implement the statistics system for the Flashcard Quizzer.

First inspect the current project structure and existing code, especially:

- utils/flashcard.py
- utils/file_handler.py
- utils/quiz_engine.py
- all existing tests
- docs/design_patterns.md
- ai_guidance/code_review_checklist.md

Do not modify documentation files.

Implement a statistics component in utils/stats.py that tracks quiz session results.

Requirements:

1. Create a clear and testable SessionStats class.
2. Track:
   - correct answers
   - incorrect answers
   - skipped answers
   - total attempted answers
3. Provide a method or property to calculate the score percentage.
4. Handle edge cases such as zero attempted answers without division-by-zero errors.
5. Use type hints and appropriate docstrings.
6. Validate inputs where appropriate.
7. Keep the class independent from terminal input/output so it can be easily unit tested.
8. Follow PEP 8 and the existing project style.

Create comprehensive tests in:

tests/test_stats.py

Include tests for:

- recording correct answers
- recording incorrect answers
- recording skipped answers
- correct total counts
- score calculation
- zero-answer edge case
- combinations of different answer types
- any invalid input or error conditions supported by the implementation

Before completing:

1. Run the new statistics tests.
2. Run the complete pytest suite.
3. Fix any test failures.
4. Run flake8 on the new and modified files.
5. Do not modify docs/ai_edit_log.md yet.

At the end, provide a concise report containing:

- files created or modified
- implementation summary
- test results
- any bugs or issues discovered
- changes made to fix those issues
- remaining integration work

Implement the phase now. You may modify project source code and test files as needed.