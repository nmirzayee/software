"""
Student Assignment Organizer
Feature: Add and validate academic assignments.

Python: 3.12+
Storage: In-memory list (assignments are not saved after exit).

v1.1 changes after agentic code review (see report, Task 5):
  - F1: EOF (Ctrl+D/Ctrl+Z) and Ctrl+C no longer crash the CLI with a traceback.
  - F2: control characters (ANSI escape sequences, newlines, bidi overrides)
        are rejected, so stored text cannot manipulate the terminal on display.
  - F3: text is Unicode-NFC normalized before length and duplicate checks.
"""
import unicodedata

MAX_COURSE_LENGTH = 30
MAX_TITLE_LENGTH = 80
SUCCESS_MESSAGE = "Assignment successfully added!"


# ---------------------------------------------------------------- validation
def _normalize(value, label):
    """Strip, NFC-normalize and reject control/format characters."""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text.")
    value = unicodedata.normalize("NFC", value.strip())
    if any(unicodedata.category(ch) in ("Cc", "Cf") for ch in value):
        raise ValueError(f"{label} contains unsupported control characters.")
    return value


def validate_assignment(course, title, assignments):
    """Validate and normalize course and assignment text.

    Returns:
        tuple[str, str]: normalized course and title.

    Raises:
        ValueError: if an input is invalid or the assignment is a duplicate.
    """
    course = _normalize(course, "Course name")
    title = _normalize(title, "Assignment title")

    # AC1: course must contain 1-30 characters after trimming.
    if not course:
        raise ValueError("Course name cannot be empty.")
    if len(course) > MAX_COURSE_LENGTH:
        raise ValueError(
            f"Course name cannot exceed {MAX_COURSE_LENGTH} characters."
        )

    # AC2: assignment title must contain 1-80 characters after trimming.
    if not title:
        raise ValueError("Assignment title cannot be empty.")
    if len(title) > MAX_TITLE_LENGTH:
        raise ValueError(
            f"Assignment title cannot exceed {MAX_TITLE_LENGTH} characters."
        )

    # AC4: duplicates are checked within the same course, ignoring case.
    for assignment in assignments:
        same_course = assignment["course"].casefold() == course.casefold()
        same_title = assignment["title"].casefold() == title.casefold()
        if same_course and same_title:
            raise ValueError("This assignment already exists in this course.")

    return course, title


# ---------------------------------------------------------------- core logic
def add_assignment(assignments, course, title):
    """Validate an assignment and append it only when all checks pass."""
    course, title = validate_assignment(course, title, assignments)

    # AC5: store one valid assignment.
    assignments.append({"course": course, "title": title})
    return SUCCESS_MESSAGE


# ---------------------------------------------------------------- output
def format_assignments(assignments):
    """Return the assignment list as display lines (pure, testable)."""
    if not assignments:
        return ["", "No assignments found."]
    lines = ["", "========== ASSIGNMENT LIST =========="]
    for number, assignment in enumerate(assignments, start=1):
        lines.append(f"{number}. Course: {assignment['course']}")
        lines.append(f"   Assignment: {assignment['title']}")
        lines.append("-------------------------------------")
    return lines


def display_assignments(assignments):
    """Print all assignments, or a message when the list is empty."""
    print("\n".join(format_assignments(assignments)))


def run_menu(assignments):
    """Command-line menu loop. Raises EOFError/KeyboardInterrupt to caller."""
    while True:
        print("\n1. Add assignment")
        print("2. View assignments")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            course = input("Enter course name: ")
            title = input("Enter assignment title: ")

            try:
                message = add_assignment(assignments, course, title)
                print(f"\nSUCCESS: {message}")
            except ValueError as error:
                # AC6: show a useful error; validation happens before mutation.
                print(f"\nERROR: {error}")

        elif choice == "2":
            display_assignments(assignments)

        elif choice == "3":
            print("\nThank you for using the application!")
            return

        else:
            print("\nERROR: Please select 1, 2 or 3.")


def main():
    """Run the command-line user interface."""
    assignments = []

    print("=====================================")
    print("     STUDENT ASSIGNMENT ORGANIZER")
    print("=====================================")

    try:
        run_menu(assignments)
    except (EOFError, KeyboardInterrupt):
        # F1: input stream closed or user pressed Ctrl+C - exit cleanly.
        print("\n\nInput ended. Exiting without changes. Goodbye!")


if __name__ == "__main__":
    main()
