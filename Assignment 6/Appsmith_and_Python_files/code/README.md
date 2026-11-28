# Student Assignment Organizer

**Coursework:** Software Engineering – Assignment 06  
**Feature:** Add and validate student assignments  
**Language:** Python 3.12  
**Editor:** Visual Studio Code  
**Operating system:** Windows 11

## 1. Project description

The Student Assignment Organizer is a command-line application for registering and viewing academic assignments. A user enters a course name and an assignment title. The application validates both values, removes leading and trailing whitespace, rejects duplicates within the same course, and displays a clear success or error message.

The project uses fictional sample data. Assignments are held in memory and are lost when the program exits.

## 2. Acceptance criteria

- **AC1 – Course validation:** After trimming, the course name must contain 1–30 characters.
- **AC2 – Title validation:** After trimming, the assignment title must contain 1–80 characters.
- **AC3 – Whitespace:** Leading and trailing whitespace is removed before storage.
- **AC4 – Duplicate detection:** The same title cannot be added twice to the same course; comparison ignores capitalization. The same title is allowed in another course.
- **AC5 – Successful addition:** A valid assignment is added exactly once and a success message is displayed.
- **AC6 – Error handling:** Invalid or duplicate input displays an error and leaves existing assignments unchanged.

## 3. Project structure

```text
StudentAssignmentOrganizer/
├── main.py
├── test_main.py
├── README.md
└── evidence/
```

## 4. Requirements

- Python 3.12 (no third-party packages required)
- Visual Studio Code or another Python editor

## 5. Run the application on Windows

Open PowerShell in this project folder and run:

```powershell
python --version
python main.py
```

If the `python` command is unavailable, try `py` instead:

```powershell
py --version
py main.py
```

Use the menu:
1. Add assignment
2. View assignments
3. Exit

## 6. Run automated tests

```powershell
python -m unittest -v
```

Or:

```powershell
py -m unittest -v
```

The test suite contains ten tests covering valid input, empty values, length limits, whitespace trimming, duplicate detection, same titles in different courses, and preservation of existing data after invalid input.

## 7. Architecture

- `validate_assignment()` checks and normalizes input.
- `add_assignment()` calls validation and updates the assignment list only after validation succeeds.
- `display_assignments()` displays stored assignments.
- `main()` provides the command-line interface.

## 8. Limitations

- Data is stored only in memory; there is no permanent database.
- There is no login, cloud synchronization, notification system, or deadline tracking.
- This is a small demonstration feature, not a production student information system.

## 9. Evidence

Place genuine screenshots from your own execution in the `evidence/` folder. Suggested evidence:
- Initial project baseline
- Successful assignment addition
- Invalid or duplicate assignment rejection
- Actual automated test output

Do not use illustrative output as proof of execution.

## 10. Version 1.1 (after agentic code review – Assignment 06, Task 5)

- F1: EOF (Ctrl+D / Ctrl+Z) and Ctrl+C exit cleanly instead of printing a traceback.
- F2: control characters (ANSI escape sequences, newlines, bidi overrides) are rejected.
- F3: text is Unicode-NFC normalized before length and duplicate checks.
- F4: 8 regression tests added (boundaries 30/80, security, EOF, output formatter) – 18 tests total.
- Output formatting moved to the pure function `format_assignments()`.

Run: `python main.py`   Tests: `python -m unittest -v`
