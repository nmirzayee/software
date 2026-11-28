import subprocess
import sys
import unicodedata
import unittest

from main import add_assignment, format_assignments


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

    # ---- added in v1.1 after agentic code review (Task 5) ----

    def test_11_course_exactly_30_characters_is_accepted(self):
        add_assignment(self.assignments, "C" * 30, "Assignment 06")
        self.assertEqual(len(self.assignments), 1)

    def test_12_title_exactly_80_characters_is_accepted(self):
        add_assignment(self.assignments, "Mathematics", "A" * 80)
        self.assertEqual(len(self.assignments), 1)

    def test_13_ansi_escape_sequence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "control characters"):
            add_assignment(
                self.assignments, "Software Engineering",
                "Lab\x1b[2J\x1b[31m FAKE: grade=A",
            )
        self.assertEqual(self.assignments, [])

    def test_14_embedded_newline_and_bidi_override_are_rejected(self):
        for course, title in (("Math\nERROR: injected", "Quiz"),
                              ("Math", "Quiz \u202e1 txt.exe")):
            with self.assertRaisesRegex(ValueError, "control characters"):
                add_assignment(self.assignments, course, title)
        self.assertEqual(self.assignments, [])

    def test_15_unicode_equivalent_title_is_duplicate(self):
        nfc = unicodedata.normalize("NFC", "Café Project")
        nfd = unicodedata.normalize("NFD", "Café Project")
        add_assignment(self.assignments, "French", nfc)
        with self.assertRaisesRegex(ValueError, "already exists"):
            add_assignment(self.assignments, "French", nfd)
        self.assertEqual(len(self.assignments), 1)

    def test_16_decomposed_characters_count_as_one(self):
        course = unicodedata.normalize("NFD", "\u00e9" * 30)
        add_assignment(self.assignments, course, "Essay")
        self.assertEqual(len(self.assignments[0]["course"]), 30)

    def test_17_eof_exits_cleanly_without_traceback(self):
        result = subprocess.run(
            [sys.executable, "-B", "main.py"], input="1\nSoftware Engineering\n",
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("Goodbye", result.stdout)

    def test_18_format_assignments_output(self):
        self.assertEqual(format_assignments([])[-1], "No assignments found.")
        add_assignment(self.assignments, "Math", "Quiz 1")
        self.assertIn("1. Course: Math", format_assignments(self.assignments))


if __name__ == "__main__":
    unittest.main(verbosity=2)
