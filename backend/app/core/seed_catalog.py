"""Static branch curricula for the development seed.

Each program has four courses per semester (theory and lab) for semesters 1–8.
Course codes are unique per institution.
"""

from __future__ import annotations

# (code, name, credits, course_type)
CourseSpec = tuple[str, str, int, str]

DEPARTMENTS: tuple[tuple[str, str], ...] = (
    ("CSE", "Computer Science and Engineering"),
    ("ECE", "Electronics and Communication Engineering"),
    ("EEE", "Electrical and Electronics Engineering"),
    ("ME", "Mechanical Engineering"),
    ("CE", "Civil Engineering"),
)

PROGRAMS: dict[str, tuple[str, str]] = {
    "CSE": ("BTECH-CSE", "B.Tech Computer Science and Engineering"),
    "ECE": ("BTECH-ECE", "B.Tech Electronics and Communication Engineering"),
    "EEE": ("BTECH-EEE", "B.Tech Electrical and Electronics Engineering"),
    "ME": ("BTECH-ME", "B.Tech Mechanical Engineering"),
    "CE": ("BTECH-CE", "B.Tech Civil Engineering"),
}

# admission year, current semester number, year of study
BATCH_PLAN: tuple[tuple[int, int, int], ...] = (
    (2026, 1, 1),
    (2025, 3, 2),
    (2024, 5, 3),
    (2023, 7, 4),
)

ACADEMIC_YEARS: tuple[tuple[str, bool], ...] = (
    ("2023-24", False),
    ("2024-25", False),
    ("2025-26", False),
    ("2026-27", True),
)

FACULTY_NAMES: tuple[str, ...] = (
    "Dr. Anil Kumar",
    "Dr. Priya Nair",
    "Prof. Ravi Shankar",
    "Prof. Sneha Rao",
    "Dr. Meera Iyer",
    "Prof. Karthik Reddy",
    "Dr. Lakshmi Menon",
    "Prof. Arjun Desai",
    "Dr. Fatima Sheikh",
    "Prof. Vikram Joshi",
    "Dr. Nandini Rao",
    "Prof. Harish Patel",
    "Dr. Divya Krishnan",
    "Prof. Suresh Babu",
    "Dr. Ananya Gupta",
    "Prof. Manoj Pillai",
    "Dr. Rekha Sharma",
    "Prof. Imran Qureshi",
    "Dr. Pooja Hegde",
    "Prof. Nikhil Verma",
    "Dr. Swathi Nambiar",
    "Prof. Deepak Chauhan",
    "Dr. Aisha Khan",
    "Prof. Rohit Malhotra",
    "Dr. Kavitha Subramanian",
    "Prof. Ajay Saxena",
    "Dr. Neha Kulkarni",
    "Prof. Sanjay Yadav",
    "Dr. Bharati Das",
    "Prof. Vivek Nair",
    "Dr. Shalini Mukherjee",
    "Prof. Gopal Krishnan",
    "Dr. Farhan Ali",
    "Prof. Jyoti Prasad",
    "Dr. Ramya Sundaram",
    "Prof. Naveen Kulkarni",
    "Dr. Tara Joseph",
    "Prof. Mohan Lal",
    "Dr. Ishita Banerjee",
    "Prof. Prakash Rao",
    "Dr. Leela Thomas",
    "Prof. Aditya Shah",
    "Dr. Geeta Menon",
    "Prof. Yusuf Ahmed",
    "Dr. Chitra Iyer",
    "Prof. Balaji Raman",
    "Dr. Hema Krishnan",
    "Prof. Sandeep Kaur",
    "Dr. Omar Farooq",
    "Prof. Lavanya Reddy",
)

FIRST_NAMES: tuple[str, ...] = (
    "Aarav", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Rohan", "Meera",
    "Vihaan", "Saanvi", "Aditya", "Anika", "Karthik", "Nisha", "Rahul", "Pooja",
    "Dev", "Shruti", "Nikhil", "Aisha", "Varun", "Lakshmi", "Siddharth", "Neha",
    "Harsh", "Riya", "Manav", "Tara", "Yash", "Isha", "Abhay", "Sneha",
    "Kunal", "Divya", "Om", "Pallavi", "Ritvik", "Anjali", "Tejas", "Myra",
)

LAST_NAMES: tuple[str, ...] = (
    "Sharma", "Patel", "Reddy", "Nair", "Iyer", "Gupta", "Khan", "Das",
    "Menon", "Joshi", "Rao", "Singh", "Kulkarni", "Banerjee", "Pillai", "Verma",
    "Chowdhury", "Hegde", "Shetty", "Mukherjee", "Bose", "Kapoor", "Naidu", "Fernandes",
    "Qureshi", "Deshmukh", "Chatterjee", "Bhat", "Malhotra", "Krishnan", "Shah", "Thomas",
    "Yadav", "Dutta", "Kaur", "Ansari", "Gowda", "Saxena", "Mathew", "Tripathi",
)

DESIGNATIONS: tuple[str, ...] = (
    "Professor",
    "Associate Professor",
    "Assistant Professor",
)


def _sem(prefix: str, rows: list[tuple[str, str, int, str]]) -> list[CourseSpec]:
    return [(f"{prefix}{code}", name, credits, ctype) for code, name, credits, ctype in rows]


CURRICULA: dict[str, list[list[CourseSpec]]] = {
    "CSE": [
        _sem("CSE", [("101", "Programming in C", 3, "THEORY"), ("102", "Engineering Mathematics I", 4, "THEORY"), ("103", "Digital Logic Design", 3, "THEORY"), ("111", "Programming in C Lab", 1, "LAB")]),
        _sem("CSE", [("201", "Data Structures", 3, "THEORY"), ("202", "Discrete Mathematics", 4, "THEORY"), ("203", "Computer Organization", 3, "THEORY"), ("211", "Data Structures Lab", 1, "LAB")]),
        _sem("CSE", [("301", "Object Oriented Programming", 3, "THEORY"), ("302", "Design and Analysis of Algorithms", 3, "THEORY"), ("303", "Database Management Systems", 3, "THEORY"), ("311", "OOP Lab", 1, "LAB")]),
        _sem("CSE", [("401", "Operating Systems", 3, "THEORY"), ("402", "Computer Networks", 3, "THEORY"), ("403", "Theory of Computation", 3, "THEORY"), ("411", "DBMS Lab", 1, "LAB")]),
        _sem("CSE", [("501", "Software Engineering", 3, "THEORY"), ("502", "Machine Learning", 3, "THEORY"), ("503", "Compiler Design", 3, "THEORY"), ("511", "Operating Systems Lab", 1, "LAB")]),
        _sem("CSE", [("601", "Artificial Intelligence", 3, "THEORY"), ("602", "Web Technologies", 3, "THEORY"), ("603", "Data Mining", 3, "THEORY"), ("611", "Web Technologies Lab", 1, "LAB")]),
        _sem("CSE", [("701", "Software Testing", 3, "THEORY"), ("702", "Information Security", 3, "THEORY"), ("703", "Cloud Computing", 3, "THEORY"), ("711", "Machine Learning Lab", 1, "LAB")]),
        _sem("CSE", [("801", "Distributed Systems", 3, "THEORY"), ("802", "Professional Ethics", 2, "THEORY"), ("803", "Project Work", 4, "THEORY"), ("811", "Project Lab", 2, "LAB")]),
    ],
    "ECE": [
        _sem("ECE", [("101", "Network Analysis", 3, "THEORY"), ("102", "Engineering Mathematics I", 4, "THEORY"), ("103", "Electronic Devices", 3, "THEORY"), ("111", "Electronics Workshop", 1, "LAB")]),
        _sem("ECE", [("201", "Digital Electronics", 3, "THEORY"), ("202", "Signals and Systems", 4, "THEORY"), ("203", "Electromagnetic Theory", 3, "THEORY"), ("211", "Digital Electronics Lab", 1, "LAB")]),
        _sem("ECE", [("301", "Analog Circuits", 3, "THEORY"), ("302", "Communication Systems", 3, "THEORY"), ("303", "Microprocessors", 3, "THEORY"), ("311", "Analog Circuits Lab", 1, "LAB")]),
        _sem("ECE", [("401", "Linear Integrated Circuits", 3, "THEORY"), ("402", "Control Systems", 3, "THEORY"), ("403", "Digital Signal Processing", 3, "THEORY"), ("411", "Communication Systems Lab", 1, "LAB")]),
        _sem("ECE", [("501", "Embedded Systems", 3, "THEORY"), ("502", "VLSI Design", 3, "THEORY"), ("503", "Antennas and Wave Propagation", 3, "THEORY"), ("511", "DSP Lab", 1, "LAB")]),
        _sem("ECE", [("601", "Wireless Communication", 3, "THEORY"), ("602", "Microwave Engineering", 3, "THEORY"), ("603", "Optical Communication", 3, "THEORY"), ("611", "Embedded Systems Lab", 1, "LAB")]),
        _sem("ECE", [("701", "Satellite Communication", 3, "THEORY"), ("702", "IoT Systems", 3, "THEORY"), ("703", "Radar Systems", 3, "THEORY"), ("711", "VLSI Lab", 1, "LAB")]),
        _sem("ECE", [("801", "Elective Advanced DSP", 3, "THEORY"), ("802", "Professional Ethics", 2, "THEORY"), ("803", "Project Work", 4, "THEORY"), ("811", "Project Lab", 2, "LAB")]),
    ],
    "EEE": [
        _sem("EEE", [("101", "Electrical Circuits", 3, "THEORY"), ("102", "Engineering Mathematics I", 4, "THEORY"), ("103", "Basic Electronics", 3, "THEORY"), ("111", "Circuits Lab", 1, "LAB")]),
        _sem("EEE", [("201", "Electromagnetic Fields", 3, "THEORY"), ("202", "Electrical Machines I", 4, "THEORY"), ("203", "Analog Electronics", 3, "THEORY"), ("211", "Machines Lab I", 1, "LAB")]),
        _sem("EEE", [("301", "Electrical Machines II", 3, "THEORY"), ("302", "Power Systems I", 3, "THEORY"), ("303", "Network Theory", 3, "THEORY"), ("311", "Machines Lab II", 1, "LAB")]),
        _sem("EEE", [("401", "Control Systems", 3, "THEORY"), ("402", "Power Electronics", 3, "THEORY"), ("403", "Measurements and Instrumentation", 3, "THEORY"), ("411", "Power Electronics Lab", 1, "LAB")]),
        _sem("EEE", [("501", "Power Systems II", 3, "THEORY"), ("502", "Microprocessors", 3, "THEORY"), ("503", "Signals and Systems", 3, "THEORY"), ("511", "Control Systems Lab", 1, "LAB")]),
        _sem("EEE", [("601", "Switchgear and Protection", 3, "THEORY"), ("602", "Electric Drives", 3, "THEORY"), ("603", "High Voltage Engineering", 3, "THEORY"), ("611", "Power Systems Lab", 1, "LAB")]),
        _sem("EEE", [("701", "Renewable Energy Systems", 3, "THEORY"), ("702", "Smart Grid", 3, "THEORY"), ("703", "Industrial Automation", 3, "THEORY"), ("711", "Drives Lab", 1, "LAB")]),
        _sem("EEE", [("801", "Elective FACTS", 3, "THEORY"), ("802", "Professional Ethics", 2, "THEORY"), ("803", "Project Work", 4, "THEORY"), ("811", "Project Lab", 2, "LAB")]),
    ],
    "ME": [
        _sem("ME", [("101", "Engineering Mechanics", 3, "THEORY"), ("102", "Engineering Mathematics I", 4, "THEORY"), ("103", "Engineering Graphics", 3, "THEORY"), ("111", "Workshop Practice", 1, "LAB")]),
        _sem("ME", [("201", "Thermodynamics", 4, "THEORY"), ("202", "Material Science", 3, "THEORY"), ("203", "Manufacturing Processes", 3, "THEORY"), ("211", "Machine Drawing Lab", 1, "LAB")]),
        _sem("ME", [("301", "Fluid Mechanics", 3, "THEORY"), ("302", "Strength of Materials", 3, "THEORY"), ("303", "Kinematics of Machinery", 3, "THEORY"), ("311", "Fluid Mechanics Lab", 1, "LAB")]),
        _sem("ME", [("401", "Heat Transfer", 3, "THEORY"), ("402", "Dynamics of Machinery", 3, "THEORY"), ("403", "Manufacturing Technology", 3, "THEORY"), ("411", "Thermal Engineering Lab", 1, "LAB")]),
        _sem("ME", [("501", "Machine Design", 4, "THEORY"), ("502", "CAD/CAM", 3, "THEORY"), ("503", "Metrology", 3, "THEORY"), ("511", "CAD Lab", 1, "LAB")]),
        _sem("ME", [("601", "Internal Combustion Engines", 3, "THEORY"), ("602", "Finite Element Methods", 3, "THEORY"), ("603", "Industrial Engineering", 3, "THEORY"), ("611", "Manufacturing Lab", 1, "LAB")]),
        _sem("ME", [("701", "Refrigeration and Air Conditioning", 3, "THEORY"), ("702", "Automobile Engineering", 3, "THEORY"), ("703", "Robotics", 3, "THEORY"), ("711", "Heat Transfer Lab", 1, "LAB")]),
        _sem("ME", [("801", "Elective Additive Manufacturing", 3, "THEORY"), ("802", "Professional Ethics", 2, "THEORY"), ("803", "Project Work", 4, "THEORY"), ("811", "Project Lab", 2, "LAB")]),
    ],
    "CE": [
        _sem("CE", [("101", "Engineering Mechanics", 3, "THEORY"), ("102", "Engineering Mathematics I", 4, "THEORY"), ("103", "Building Materials", 3, "THEORY"), ("111", "Engineering Drawing Lab", 1, "LAB")]),
        _sem("CE", [("201", "Surveying", 3, "THEORY"), ("202", "Strength of Materials", 4, "THEORY"), ("203", "Fluid Mechanics", 3, "THEORY"), ("211", "Surveying Lab", 1, "LAB")]),
        _sem("CE", [("301", "Structural Analysis", 3, "THEORY"), ("302", "Concrete Technology", 3, "THEORY"), ("303", "Hydraulics", 3, "THEORY"), ("311", "Strength of Materials Lab", 1, "LAB")]),
        _sem("CE", [("401", "Geotechnical Engineering", 3, "THEORY"), ("402", "Transportation Engineering", 3, "THEORY"), ("403", "Environmental Engineering", 3, "THEORY"), ("411", "Fluid Mechanics Lab", 1, "LAB")]),
        _sem("CE", [("501", "Design of RCC Structures", 4, "THEORY"), ("502", "Foundation Engineering", 3, "THEORY"), ("503", "Water Resources Engineering", 3, "THEORY"), ("511", "Geotechnical Lab", 1, "LAB")]),
        _sem("CE", [("601", "Design of Steel Structures", 3, "THEORY"), ("602", "Highway Engineering", 3, "THEORY"), ("603", "Estimation and Costing", 3, "THEORY"), ("611", "Environmental Engineering Lab", 1, "LAB")]),
        _sem("CE", [("701", "Prestressed Concrete", 3, "THEORY"), ("702", "Irrigation Engineering", 3, "THEORY"), ("703", "Construction Management", 3, "THEORY"), ("711", "Concrete Lab", 1, "LAB")]),
        _sem("CE", [("801", "Elective Earthquake Engineering", 3, "THEORY"), ("802", "Professional Ethics", 2, "THEORY"), ("803", "Project Work", 4, "THEORY"), ("811", "Project Lab", 2, "LAB")]),
    ],
}


def program_for(dept_code: str) -> tuple[str, str]:
    return PROGRAMS[dept_code]
