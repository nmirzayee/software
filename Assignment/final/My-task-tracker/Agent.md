
# Agent.md – Repository Instructions

## 1. Project Purpose

Simple Task Tracker is a small Python command-line application for managing daily tasks.

The application allows users to:
- Add new tasks.
- Display existing tasks.
- Mark tasks as completed.
- Delete tasks.
- Save task information in JSON format.

The project must remain a command-line application. Do not convert it into a website or add a web framework.

## 2. Project Architecture

The repository has the following structure:

```text
simple_task_tracker/
├── task_tracker/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_app.py
├── README.md
├── requirement.txt
├── Agent.md
└── .gitignore
```

### Main files

- `task_tracker/app.py`: Contains application logic, task operations, JSON file handling, and command-line interface.
- `tests/test_app.py`: Contains automated tests.
- `README.md`: Contains project documentation and usage instructions.
- `requirement.txt`: Lists external dependencies.
- `Agent.md`: Provides instructions and operating boundaries for coding agents.

Keep application logic inside the `task_tracker` package and automated tests inside the `tests` directory.

## 3. Development Environment Setup

Requirements:
- Python 3.10 or newer.
- pip.
- pytest for automated testing.

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install testing dependencies:

```bash
py -m pip install pytest
```

If the project has additional dependencies listed in `requirement.txt`, install them using:

```bash
py -m pip install -r requirement.txt
```

Use `py` for Python commands on Windows. Do not install or update dependencies
unless the approved task requires it, and do not add unnecessary dependencies.

## 4. Safe Commands

The following commands are permitted for normal development and verification:

Check Python version:

```bash
py --version
```

Run automated tests:

```bash
py -m pytest -v
```

Check Python compilation:

```bash
py -m compileall task_tracker
```

Run the application:

```bash
py -m task_tracker.app
```

Add a task:

```bash
py -m task_tracker.app add "Study Python"
```

Display tasks:

```bash
py -m task_tracker.app list
```

Complete a task:

```bash
py -m task_tracker.app done 1
```

Delete a task:

```bash
py -m task_tracker.app delete 1
```

Check repository status:

```bash
git status
```

Inspect commit history:

```bash
git log --oneline
```

Before changing files, inspect the existing implementation and understand its behavior.
Use only commands needed for the approved task. Do not run destructive commands
without explicit human approval.

## 5. Coding Conventions

All Python code should follow these conventions:

- Use clear and descriptive function and variable names.
- Follow standard Python naming conventions.
- Use four spaces for indentation.
- Keep functions small and focused on one responsibility.
- Avoid unnecessary code duplication.
- Add comments or docstrings when they improve understanding.
- Handle invalid user input appropriately.
- Handle JSON and file errors safely.
- Keep changes simple and consistent with the existing architecture.
- Do not change existing behavior unless the task requires it.

Avoid introducing design patterns or additional abstractions without a clear maintainability benefit.

## 6. Test Expectations

Every change must be checked before it is accepted.

The automated tests should verify:

1. Adding a task works correctly.
2. Existing tasks can be displayed.
3. Tasks can be marked as completed.
4. Existing tasks can be deleted.
5. Empty task titles are rejected.
6. Invalid input and file-handling situations are handled appropriately.

Run the tests using:

```bash
py -m pytest -v
```

Run compilation checks using:

```bash
py -m compileall task_tracker
```

Do not claim that tests passed unless they have actually been executed.

If a test fails, investigate the cause and report the failure instead of hiding it.

## 7. Forbidden Actions and Safety Boundaries

Coding agents must follow these restrictions:

- Never read, expose, or upload passwords, API keys, tokens, or other secrets.
- Never upload private project data to external services or introduce unnecessary network access.
- Never add real personal or sensitive information to the repository.
- Never deploy the application to production.
- Never run destructive commands without explicit human approval.
- Never delete project files or important user data without approval.
- Never overwrite existing user changes, backups, or user data.
- Never make dependency changes without explaining and obtaining human review.
- Modify only files required for the approved task; never modify unrelated files.
- Never overwrite the original project without preserving a recoverable version.
- Never commit, push, deploy, or publish without explicit human approval.
- Never accept AI-generated code without reviewing it.

Do not execute commands that can delete files, reset Git history, or overwrite important data unless the user explicitly authorizes the action.

## 8. Change Review Process

Before making changes:

1. Inspect the relevant files.
2. Check `git status` and inspect the current branch before editing.
3. Use a separate working branch for each significant task. If creating or
   switching branches could affect existing user changes, stop and ask first.
4. Understand the current implementation and identify the problem being solved.
5. Confirm the task scope and any time limit. Do not expand scope without approval.
6. Ask before making changes outside the approved scope.

After making changes:

1. Review the complete code changes.
2. Check for unrelated modifications.
3. Run relevant automated tests and compilation checks when appropriate.
4. Report commands and actual results; never claim checks passed unless they ran.
5. Explain remaining problems and limitations.

Provide the complete Git diff for human review. If a test fails, a command
behaves unexpectedly, or a change causes a problem, stop further modifications.
Show the relevant error or diff, explain what happened, and recommend a safe
correction; do not hide or silently ignore failures. If the task cannot be
completed safely or within its defined time limit, stop and report why.

Do not commit, push, deploy, publish, or merge without explicit human approval.

Every completed task report must include:

- Summary of work and modified files.
- The complete Git diff.
- Commands executed and actual test results, including failures.
- Remaining risks and limitations.
- Any actions requiring human approval.

## 9. General Agent Instructions

Keep the project small, readable, and maintainable.

Preserve the original command-line interface and JSON storage approach.

Do not introduce Flask, Django, frontend frameworks, databases, hosting services, or unnecessary external tools.

Preserve the Task 3 `_find_task()` helper and the Task 7 JSON validation and
safer JSON saving improvements unless the approved task explicitly requires
changing them.

Prioritize correctness, security, simplicity, and test coverage.
