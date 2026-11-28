# Student Assignment Organizer

**Coursework:** Software Engineering – Assignment 06  
**Feature:** Add and validate student assignments  
**Language:** Python 3.12  
**Editor:** Visual Studio Code  
**Operating system:** Windows 11

## 1. Project description

The Student Assignment Organizer is a command-line application for registering and viewing academic assignments. A user enters a course name and an assignment title. The application validates both values, removes leading and trailing whitespace, rejects duplicates within the same course, and displays a clear success or error message.

The project uses fictional sample data. Assignments are held in memory and are lost when the program exits.

## Baseline and requirements

### Baseline

The pre-implementation baseline was the initial planning state: the assignment-management feature had not yet been implemented. This is a historical reference, not a description of the current application.

No original pre-implementation screenshot or saved project copy is included in the available project files. Do not present a screenshot of the implemented application as original baseline evidence. If a screenshot is captured now, label it as current project-state evidence.

### Inputs and validation

| Input | Rule after trimming leading and trailing whitespace |
|---|---|
| Course name | Required; 1–30 characters |
| Assignment title | Required; 1–80 characters |

Duplicate titles are rejected within the same course, ignoring capitalization. The same title is allowed in another course. Failed additions must not change the existing assignment list.

### Expected messages

| Situation | Expected message |
|---|---|
| Valid assignment | `Assignment successfully added!` |
| Empty course | `Course name cannot be empty.` |
| Course over 30 characters | `Course name cannot exceed 30 characters.` |
| Empty assignment title | `Assignment title cannot be empty.` |
| Title over 80 characters | `Assignment title cannot exceed 80 characters.` |
| Duplicate title in the same course | `This assignment already exists in this course.` |

### Sample cases

| Course | Assignment title | Expected result |
|---|---|---|
| Software Engineering | Assignment 06 | Accepted |
| Mathematics | Homework 01 | Accepted |
| Computer Architecture | Lecture Notes | Accepted |
| *(empty)* | Assignment 02 | Rejected: empty course |
| Software Engineering | Assignment 06 (after its first addition) | Rejected: duplicate |
| Software Engineering | Assignment 07 | Accepted |
| Mathematics | Assignment 06 | Accepted: different course |

The project brief describes both a Python and a MIT App Inventor implementation. The files currently present in this project folder provide the Python implementation; no App Inventor project file is included here.

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
└── README.md
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
