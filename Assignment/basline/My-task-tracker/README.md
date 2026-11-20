# Simple Task Tracker

A small Python command-line application for managing personal tasks. It stores tasks in a local JSON file.

## Features
- Add a task
- List all tasks
- Mark a task as completed
- Delete a task
- Reject empty task titles

## Requirements
- Python 3.9 or newer
- pytest (only for running tests)

## Setup
Open a terminal in the project folder:

```bash
python --version
python -m pip install pytest
```

## Run the application

```bash
python -m task_tracker.app add "Study Python"
python -m task_tracker.app list
python -m task_tracker.app done 1
python -m task_tracker.app delete 1
```

The application creates `tasks.json` in the current working directory when you add the first task.

## Run tests

```bash
python -m pytest -v
```

## Project structure

```text
simple_task_tracker/
├── task_tracker/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_app.py
└── README.md
```

## Acceptance criteria
1. A user can add a task with a non-empty title.
2. A user can list saved tasks.
3. A user can mark an existing task as completed.
4. A user can delete an existing task.
5. The application reports an error for an empty title or missing task ID.
