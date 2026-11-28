import unittest

from main import add_assignment


class TestStudentAssignmentOrganizer(unittest.TestCase):

    def setUp(self):
        self.assignments = []

    def test_01_valid_assignment_is_added(self):
        result = add_assignment(
            self.assignments, "Software Engineering", "Assignment 06"
        )
        self.assertEqual(result, "Assignment successfully added!")
        self.assertEqual(
            self.assignments,
            [{"course": "Software Engineering", "title": "Assignment 06"}],
        )

    def test_02_empty_course_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Course name cannot be empty"):
            add_assignment(self.assignments, "   ", "Assignment 06")
        self.assertEqual(self.assignments, [])

    def test_03_empty_title_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError, "Assignment title cannot be empty"
        ):
            add_assignment(self.assignments, "Software Engineering", "  ")
        self.assertEqual(self.assignments, [])

    def test_04_course_over_30_characters_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError, "Course name cannot exceed 30 characters"
        ):
            add_assignment(self.assignments, "C" * 31, "Assignment 06")

    def test_05_title_over_80_characters_is_rejected(self):
        with self.assertRaisesRegex(
            ValueError, "Assignment title cannot exceed 80 characters"
        ):
            add_assignment(self.assignments, "Mathematics", "A" * 81)

    def test_06_leading_and_trailing_spaces_are_removed(self):
        add_assignment(
            self.assignments, "  Software Engineering  ", "  Assignment 06  "
        )
        self.assertEqual(
            self.assignments[0],
            {"course": "Software Engineering", "title": "Assignment 06"},
        )

    def test_07_exact_duplicate_is_rejected(self):
        add_assignment(self.assignments, "Software Engineering", "Assignment 06")
        before = [item.copy() for item in self.assignments]
        with self.assertRaisesRegex(ValueError, "already exists"):
            add_assignment(
                self.assignments, "Software Engineering", "Assignment 06"
            )
        self.assertEqual(self.assignments, before)

    def test_08_duplicate_ignores_capitalization(self):
        add_assignment(self.assignments, "Software Engineering", "Assignment 06")
        with self.assertRaisesRegex(ValueError, "already exists"):
            add_assignment(
                self.assignments, "software engineering", "assignment 06"
            )
        self.assertEqual(len(self.assignments), 1)

    def test_09_same_title_in_different_course_is_allowed(self):
        add_assignment(self.assignments, "Software Engineering", "Assignment 01")
        add_assignment(self.assignments, "Computer Architecture", "Assignment 01")
        self.assertEqual(len(self.assignments), 2)

    def test_10_invalid_input_preserves_existing_assignments(self):
        add_assignment(self.assignments, "Software Engineering", "Assignment 06")
        before = [item.copy() for item in self.assignments]
        with self.assertRaises(ValueError):
            add_assignment(self.assignments, "Software Engineering", "")
        self.assertEqual(self.assignments, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
