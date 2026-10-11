"""SQLAlchemy models package."""

from app.models.academic_year import AcademicYear
from app.models.batch import Batch
from app.models.class_group import ClassGroup
from app.models.course import Course
from app.models.course_backlog import CourseBacklog
from app.models.department import Department
from app.models.enrollment import (
    Assessment,
    AssessmentMark,
    Attendance,
    CourseResult,
    Enrollment,
    SemesterResult,
)
from app.models.faculty import Faculty
from app.models.faculty_course import FacultyCourse
from app.models.import_job import ImportJob
from app.models.institution import Institution
from app.models.parent import FacultyStudent, Parent, ParentStudent
from app.models.prediction import PredictionResult, StudentGoal
from app.models.program import Program
from app.models.program_course import ProgramCourse
from app.models.section import Section
from app.models.semester import Semester
from app.models.student import Student
from app.models.user import User

__all__ = [
    "AcademicYear",
    "Assessment",
    "AssessmentMark",
    "Attendance",
    "Batch",
    "ClassGroup",
    "Course",
    "CourseBacklog",
    "CourseResult",
    "Department",
    "Enrollment",
    "Faculty",
    "FacultyCourse",
    "FacultyStudent",
    "ImportJob",
    "Institution",
    "Parent",
    "ParentStudent",
    "PredictionResult",
    "Program",
    "ProgramCourse",
    "Section",
    "Semester",
    "SemesterResult",
    "Student",
    "StudentGoal",
    "User",
]
