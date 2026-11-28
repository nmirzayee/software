


def validate_assignment(course, title, assignments):
    """Validate and normalize course and assignment text.

    Returns:
        tuple[str, str]: normalized course and title.

    Raises:
        ValueError: if an input is invalid or the assignment is a duplicate.
    """
    if not isinstance(course, str):
        raise ValueError("Course name must be text.")
    if not isinstance(title, str):
        raise ValueError("Assignment title must be text.")

    course = course.strip()
    title = title.strip()

    # AC1: course must contain 1-30 characters after trimming.
    if not course:
        raise ValueError("Course name cannot be empty.")
    if len(course) > 30:
        raise ValueError("Course name cannot exceed 30 characters.")

    # AC2: assignment title must contain 1-80 characters after trimming.
    if not title:
        raise ValueError("Assignment title cannot be empty.")
    if len(title) > 80:
        raise ValueError("Assignment title cannot exceed 80 characters.")

    # AC4: duplicates are checked within the same course, ignoring case.
    for assignment in assignments:
        same_course = assignment["course"].casefold() == course.casefold()
        same_title = assignment["title"].casefold() == title.casefold()
        if same_course and same_title:
            raise ValueError(
                "This assignment already exists in this course."
            )

    return course, title


def add_assignment(assignments, course, title):
    """Validate an assignment and append it only when all checks pass."""
    course, title = validate_assignment(course, title, assignments)

    # AC5: store one valid assignment.
    assignments.append({"course": course, "title": title})
    return "Assignment successfully added!"


def display_assignments(assignments):
    """Print all assignments, or a message when the list is empty."""
    if not assignments:
        print("\nNo assignments found.")
        return

    print("\n========== ASSIGNMENT LIST ==========")
    for number, assignment in enumerate(assignments, start=1):
        print(f"{number}. Course: {assignment['course']}")
        print(f"   Assignment: {assignment['title']}")
        print("-------------------------------------")


def main():
    """Run the command-line user interface."""
    assignments = []

    print("=====================================")
    print("     STUDENT ASSIGNMENT ORGANIZER")
    print("=====================================")

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
            break

        else:
            print("\nERROR: Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()
