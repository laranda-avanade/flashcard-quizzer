Implement Phase 2 only: the quiz engine and design patterns.

First inspect the current Phase 1 implementation so the new code integrates correctly.

Do not modify the completed Phase 1 files unless absolutely necessary to fix an integration issue.

Create or implement:

- utils/quiz_engine.py

Requirements:

1. Use the Strategy Pattern.
   Create an abstract base class named QuizMode.

2. Create these concrete strategies:
   - SequentialMode
   - RandomMode
   - AdaptiveMode

3. SequentialMode:
   - Present cards in their original order.
   - Each card should be selected exactly once during a normal session.

4. RandomMode:
   - Present every card exactly once in shuffled order.
   - Do not repeat cards.
   - Make the implementation testable and deterministic when needed.

5. AdaptiveMode:
   - Prioritize cards answered incorrectly.
   - The behavior must actually repeat incorrectly answered cards.
   - Avoid the previous proposal where weighted random selection could fail to repeat a missed card.
   - Use a clear and deterministic approach that can be tested.

Recommended behavior:
   - Start by presenting cards from the deck.
   - When a card is answered incorrectly, place it into a retry queue.
   - Retry incorrectly answered cards according to a clearly defined rule.
   - A card should stop repeating after it is answered correctly.
   - Ensure the session always terminates and cannot enter an infinite loop.

6. The strategy interface should be appropriate for integration with a future quiz session and should support tracking answer results.

7. Implement a Factory Pattern:
   - QuizModeFactory
   - Accept mode names such as "sequential", "random", and "adaptive".
   - Return the correct strategy object.
   - Handle invalid modes with a helpful ValueError.

8. Use complete Python type hints and appropriate docstrings.

9. Keep the design simple. Do not create unnecessary files or abstractions.

Testing:

Create tests/test_quiz_modes.py covering at minimum:

- Sequential mode returns cards in original order.
- Random mode includes every card exactly once.
- Random behavior can be tested deterministically.
- QuizModeFactory returns the correct strategy class.
- Invalid mode raises a helpful error.
- Adaptive mode actually repeats incorrectly answered cards.
- Adaptive mode stops repeating a card after it is answered correctly.
- Adaptive mode terminates correctly without an infinite loop.

Before editing, state the files you will modify.

Then implement the code and tests.

After implementation, run:

python -m pytest tests/ -v

Run flake8 on the files changed if available.

Report:
- files changed
- test results
- flake8 results
- a brief explanation of the AdaptiveMode algorithm

Do not implement the CLI, UI, argparse, or session statistics yet.