You are helping me develop the Udacity AI-Powered Software Engineer project: "The Flashcard Quizzer" CLI application.

First, inspect the existing repository and understand the starter project before making any changes.

IMPORTANT:
- Do NOT modify, create, delete, or rename any files yet.
- Do NOT write implementation code yet.
- Do NOT remove or restructure the provided folders.
- Treat the existing starter repository structure and provided templates as authoritative.

Please inspect:
1. The complete current directory and file structure.
2. The contents of main.py.
3. The contents of the data/, utils/, tests/, and docs/ directories.
4. README.md and any other project documentation.
5. Any configuration files such as requirements.txt, pyproject.toml, .claude/, .env, or similar files if present.

After inspecting the repository, provide:

1. A concise summary of the current starter project.
2. The purpose of each existing relevant file and directory.
3. Any existing code or templates that should be preserved.
4. Any missing components that will need to be implemented.
5. A proposed modular architecture for the Flashcard Quizzer.
6. A proposed development sequence broken into small implementation phases.
7. Potential technical risks or areas where AI-generated code could easily be incorrect.

The application requirements include:
- Loading flashcards from JSON.
- Supporting both:
  [{"front": "...", "back": "..."}]
  and:
  {"cards": [{"front": "...", "back": "..."}]}
- Friendly handling of missing, malformed, or invalid JSON.
- Sequential, Random, and Adaptive quiz modes.
- Strategy Pattern for quiz modes.
- Factory Pattern for selecting the quiz mode.
- Case-insensitive answer checking.
- Session statistics.
- argparse with -f, -m, and --stats.
- Green correct feedback and red incorrect feedback.
- Graceful "exit" and Ctrl+C handling.
- Python type hints.
- pytest tests with more than 80% coverage.
- PEP 8 and flake8 compliance.

Do not implement anything yet. I want to review your analysis and architecture proposal first.

