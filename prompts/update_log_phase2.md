Please update docs/ai_edit_log.md by adding a new detailed entry for
today's Phase 2 development work.

Do not modify any other files.

Use the existing AI Edit Log template and create an entry describing
the implementation of the quiz engine using the Strategy and Factory
design patterns.

Include the following information:

Context:
I needed to implement the quiz mode system for the Flashcard Quizzer.
The application needed Sequential, Random, and Adaptive quiz modes.
The implementation also needed to satisfy the design pattern
requirement from the project rubric.

AI Tool Used:
Claude Code.

Prompt/Request:
Summarize that I asked Claude to implement the Phase 2 quiz engine
and its tests based on the previously approved architecture.

AI Response:
Claude created utils/quiz_engine.py and tests/test_quiz_modes.py.
The implementation included quiz mode classes and tests for their
behavior.

Changes Made:
Document the three issues discovered during testing:

1. Tests attempted to use set() with Flashcard objects, causing a
TypeError because Flashcard dataclass instances were not hashable.
This was changed to a sorted comparison using the front field.

2. AdaptiveMode had an infinite-loop risk because a card that was
answered incorrectly could be re-added and consumed again during the
same retry pass. The algorithm was modified so re-enqueued cards are
deferred to the next retry pass.

3. One termination test incorrectly assumed the quiz would terminate
even if every answer remained incorrect forever. That test assumption
was rejected and replaced with a realistic test where cards are
answered incorrectly a limited number of times before eventually being
answered correctly.

Reasoning:
Explain that AI-generated code and tests must be validated rather than
accepted automatically. The changes were necessary to avoid incorrect
tests and a potential unbounded retry loop.

Outcome:
69 tests passed with 0 failures. Flake8 passed after fixing one E501
long line. The quiz engine and its tests were successfully completed.

Lessons Learned:
Mention that AI can generate useful implementations quickly, but
algorithm behavior and test assumptions still require human review.
Testing exposed issues that were not obvious during code generation.

Do not change existing entries. Append this as a new entry only.