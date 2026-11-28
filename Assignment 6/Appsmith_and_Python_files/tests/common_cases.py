"""Common test suite (Task 4). Identical inputs for the code-based and low-code versions.

Each case: preconditions (assignments entered first, all valid) and one action.
Expected: whether the action is stored, the expected message, and the expected
number of stored assignments afterwards.
"""
C30 = "Cloud Computing Fundamentals 1"          # exactly 30 characters
C31 = "Cloud Computing Fundamentals 12"         # 31 characters
T80 = "Final Project Report " + "x" * 59        # exactly 80 characters
T81 = T80 + "y"                                  # 81 characters
assert len(C30) == 30 and len(C31) == 31 and len(T80) == 80 and len(T81) == 81

OK = "Assignment successfully added!"
CASES = [
    dict(id="TC01", name="Normal valid assignment", type="Normal",
         pre=[], course="Software Engineering", title="Assignment 06",
         stored=True, msg=OK, count=1, store_as=("Software Engineering", "Assignment 06")),
    dict(id="TC02", name="Leading/trailing whitespace trimmed", type="Normal",
         pre=[], course="  Computer Architecture  ", title="  Lab 3 Report  ",
         stored=True, msg=OK, count=1, store_as=("Computer Architecture", "Lab 3 Report")),
    dict(id="TC03", name="Upper boundary accepted (30 / 80 chars)", type="Boundary",
         pre=[], course=C30, title=T80, stored=True, msg=OK, count=1, store_as=(C30, T80)),
    dict(id="TC04", name="Course 31 chars rejected", type="Boundary/invalid",
         pre=[("Mathematics", "Problem Set 1")], course=C31, title="Quiz 1",
         stored=False, msg="Course name cannot exceed 30 characters.", count=1),
    dict(id="TC05", name="Title 81 chars rejected", type="Boundary/invalid",
         pre=[("Mathematics", "Problem Set 1")], course="Mathematics", title=T81,
         stored=False, msg="Assignment title cannot exceed 80 characters.", count=1),
    dict(id="TC06", name="Whitespace-only course rejected", type="Invalid",
         pre=[("Mathematics", "Problem Set 1")], course="   ", title="Assignment 06",
         stored=False, msg="Course name cannot be empty.", count=1),
    dict(id="TC07", name="Whitespace-only title rejected", type="Invalid",
         pre=[("Mathematics", "Problem Set 1")], course="Software Engineering", title="   ",
         stored=False, msg="Assignment title cannot be empty.", count=1),
    dict(id="TC08", name="Repeated identical add rejected", type="Repeated operation",
         pre=[("Software Engineering", "Assignment 06")], course="Software Engineering",
         title="Assignment 06", stored=False,
         msg="This assignment already exists in this course.", count=1),
    dict(id="TC09", name="Duplicate ignoring capitalization rejected", type="Repeated/invalid",
         pre=[("Software Engineering", "Assignment 06")], course="software engineering",
         title="ASSIGNMENT 06", stored=False,
         msg="This assignment already exists in this course.", count=1),
    dict(id="TC10", name="Same title in another course accepted", type="Normal",
         pre=[("Software Engineering", "Assignment 06")], course="Computer Architecture",
         title="Assignment 06", stored=True, msg=OK, count=2,
         store_as=("Computer Architecture", "Assignment 06")),
    dict(id="TC11", name="Inner spaces kept; not a duplicate", type="Boundary (normalization)",
         pre=[("Software Engineering", "Assignment 06")], course="Software Engineering",
         title="Assignment  06", stored=True, msg=OK, count=2,
         store_as=("Software Engineering", "Assignment  06")),
    dict(id="TC12", name="Error after valid data leaves list unchanged", type="Error feedback",
         pre=[("Software Engineering", "Assignment 06"), ("Mathematics", "Problem Set 1")],
         course="Mathematics", title="problem set 1", stored=False,
         msg="This assignment already exists in this course.", count=2),
]
