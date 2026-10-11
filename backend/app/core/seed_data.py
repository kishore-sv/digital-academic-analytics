"""Canonical seed institution names and default credentials for development.

These passwords are for local development only. They are not used by production code.
"""

INSTITUTION_1_NAME = "Demo University"
INSTITUTION_2_NAME = "Riverside College of Engineering"

# Institution 1 — primary tenant (Demo University)
ADMIN_EMAIL = "admin@demo.com"
ADMIN_PASSWORD = "admin123"
FACULTY_EMAIL = "faculty@demo.com"
FACULTY_PASSWORD = "faculty123"
PARENT_EMAIL = "parent@demo.com"
PARENT_PASSWORD = "parent123"
STUDENT_PASSWORD = "student123"

# Pinned students inside the deterministic 2,400-student dataset.
# 26CSE001 year 1 (high), 25CSE001 year 2 (average), 24CSE001 year 3 (at-risk).
STUDENT_ROLLS = (
    ("26CSE001", "Kishore S V"),
    ("25CSE001", "Srivatsa Kamble"),
    ("24CSE001", "Mohan A"),
)

PINNED_PROFILES = {
    "26CSE001": "high",
    "25CSE001": "average",
    "24CSE001": "at_risk",
}

# Institution 2 — tenant isolation tests
ADMIN_2_EMAIL = "admin@riverside.edu"
ADMIN_2_PASSWORD = "admin123"
STUDENT_2_ROLL = "20231ECE9999"
STUDENT_2_NAME = "Riverside Student"

DEPARTMENTS = (
    ("CSE", "Computer Science and Engineering"),
    ("ECE", "Electronics and Communication Engineering"),
    ("EEE", "Electrical and Electronics Engineering"),
    ("ME", "Mechanical Engineering"),
    ("CE", "Civil Engineering"),
)

SAMPLE_FACULTY_EMPLOYEE_ID = "FAC-CSE-01"
SAMPLE_PARENT_EMAIL = "parent@demo.com"
