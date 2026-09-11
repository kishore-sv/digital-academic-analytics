"""Canonical seed institution names and default credentials for development."""

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

STUDENT_ROLLS = (
    ("20231CSE0260", "Kishore S V"),
    ("20231CSE0257", "Srivatsa Kamble"),
    ("20231CSE0273", "Mohan A"),
)

# Institution 2 — tenant isolation tests
ADMIN_2_EMAIL = "admin@riverside.edu"
ADMIN_2_PASSWORD = "admin123"
STUDENT_2_ROLL = "20231ECE9999"

DEPARTMENTS = (
    ("CSE", "Computer Science & Engineering"),
    ("ECE", "Electronics & Communication Engineering"),
    ("IST", "Information Science & Technology"),
    ("EEE", "Electrical & Electronics"),
    ("MECH", "Mechanical Engineering"),
    ("CIVIL", "Civil Engineering"),
)
