"""Academic entity request/response schemas."""

from datetime import date as DateType
from datetime import datetime

from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.academic_display import format_year_number

CourseTypeLiteral = Literal["THEORY", "LAB"]


# Institution
class InstitutionResponse(BaseModel):
    id: str
    name: str
    logo_url: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}


class InstitutionUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    description: str | None = None


# User
class UserResponse(BaseModel):
    id: str
    email: str | None
    role: str
    institution_id: str
    is_login_enabled: bool

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="institution_admin", pattern="^institution_admin$")


class UserUpdate(BaseModel):
    is_login_enabled: bool | None = None


# Department
class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: str | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None


class DepartmentResponse(BaseModel):
    id: str
    name: str
    code: str
    description: str | None = None

    model_config = {"from_attributes": True}


# Program
class ProgramCreate(BaseModel):
    department_id: str
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    duration_semesters: int = Field(default=8, ge=1, le=12)


class ProgramUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    duration_semesters: int | None = Field(default=None, ge=1, le=12)


class ProgramResponse(BaseModel):
    id: str
    department_id: str
    name: str
    code: str
    duration_semesters: int

    model_config = {"from_attributes": True}


# Academic Year
class AcademicYearCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    is_current: bool = False


class AcademicYearUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    is_current: bool | None = None


class AcademicYearResponse(BaseModel):
    id: str
    name: str
    is_current: bool

    model_config = {"from_attributes": True}


# Semester
class SemesterCreate(BaseModel):
    academic_year_id: str
    number: int = Field(..., ge=1, le=12)
    name: str = Field(..., min_length=1, max_length=100)
    year_number: int = Field(..., ge=1, le=8)


class SemesterUpdate(BaseModel):
    number: int | None = Field(default=None, ge=1, le=12)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    year_number: int | None = Field(default=None, ge=1, le=8)


class SemesterResponse(BaseModel):
    id: str
    academic_year_id: str
    number: int
    name: str
    year_number: int
    year_label: str | None = None

    model_config = {"from_attributes": True}

    @field_validator("year_label", mode="before")
    @classmethod
    def compute_year_label(cls, v, info):
        if v is not None:
            return v
        data = info.data
        if "year_number" in data:
            return format_year_number(data["year_number"])
        return None


# Batch
class BatchCreate(BaseModel):
    program_id: str
    admission_year: int = Field(..., ge=2000, le=2100)
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True


class BatchUpdate(BaseModel):
    admission_year: int | None = Field(default=None, ge=2000, le=2100)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class BatchResponse(BaseModel):
    id: str
    program_id: str
    admission_year: int
    code: str
    name: str
    is_active: bool

    model_config = {"from_attributes": True}


# Class Group
class ClassGroupCreate(BaseModel):
    batch_id: str
    year_number: int = Field(..., ge=1, le=8)
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)


class ClassGroupUpdate(BaseModel):
    year_number: int | None = Field(default=None, ge=1, le=8)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)


class ClassGroupResponse(BaseModel):
    id: str
    batch_id: str
    year_number: int
    year_label: str | None = None
    code: str
    name: str

    model_config = {"from_attributes": True}


# Section
class SectionCreate(BaseModel):
    class_group_id: str
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=255)
    is_active: bool = True


class SectionUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class SectionResponse(BaseModel):
    id: str
    class_group_id: str
    code: str
    name: str
    is_active: bool

    model_config = {"from_attributes": True}


# Program Course (curriculum)
class ProgramCourseCreate(BaseModel):
    program_id: str
    course_id: str
    semester_number: int = Field(..., ge=1, le=12)


class ProgramCourseUpdate(BaseModel):
    semester_number: int | None = Field(default=None, ge=1, le=12)


class ProgramCourseResponse(BaseModel):
    id: str
    program_id: str
    course_id: str
    semester_number: int

    model_config = {"from_attributes": True}


# Faculty Course assignment
class FacultyCourseCreate(BaseModel):
    faculty_id: str
    course_id: str
    semester_id: str
    section_id: str | None = None


class FacultyCourseUpdate(BaseModel):
    section_id: str | None = None


class FacultyCourseResponse(BaseModel):
    id: str
    faculty_id: str
    course_id: str
    semester_id: str
    section_id: str | None = None

    model_config = {"from_attributes": True}


# Faculty
class FacultyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    department_id: str
    employee_id: str = Field(..., min_length=1, max_length=50)
    designation: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=30)


class FacultyUpdate(BaseModel):
    name: str | None = None
    department_id: str | None = None
    employee_id: str | None = Field(default=None, min_length=1, max_length=50)
    designation: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=30)


class FacultyResponse(BaseModel):
    id: str
    name: str
    email: str | None = None
    department_id: str
    user_id: str
    employee_id: str
    designation: str | None = None
    phone: str | None = None

    model_config = {"from_attributes": True}


# Parent
class ParentStudentLink(BaseModel):
    student_id: str
    relationship_type: str = Field(default="GUARDIAN", max_length=30)
    is_primary_guardian: bool = False


class ParentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: str | None = Field(default=None, max_length=30)
    student_links: list[ParentStudentLink] = Field(default_factory=list)


class ParentUpdate(BaseModel):
    name: str | None = None
    phone: str | None = Field(default=None, max_length=30)


class ParentResponse(BaseModel):
    id: str
    name: str
    user_id: str
    phone: str | None = None
    linked_student_ids: list[str] = []
    student_links: list[ParentStudentLink] = []

    model_config = {"from_attributes": True}


# Student
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    roll_number: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)
    department_id: str
    program_id: str
    batch_id: str
    class_group_id: str
    section_id: str
    current_semester_id: str
    admission_date: DateType | None = None


class StudentUpdate(BaseModel):
    name: str | None = None
    department_id: str | None = None
    program_id: str | None = None
    batch_id: str | None = None
    class_group_id: str | None = None
    section_id: str | None = None
    current_semester_id: str | None = None
    admission_date: DateType | None = None


class StudentSemesterSummary(BaseModel):
    id: str
    number: int
    name: str
    year_number: int
    year_label: str


class StudentResponse(BaseModel):
    id: str
    roll_number: str
    name: str
    department_id: str
    program_id: str
    batch_id: str
    class_group_id: str
    section_id: str
    current_semester_id: str
    admission_date: DateType | None = None
    semester_number: int | None = None
    year_number: int | None = None
    year_label: str | None = None
    section_code: str | None = None
    batch_name: str | None = None

    model_config = {"from_attributes": True}


# Course
class CourseCreate(BaseModel):
    department_id: str
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    credits: int = Field(default=3, ge=1, le=6)
    course_type: CourseTypeLiteral = "THEORY"


class CourseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    credits: int | None = Field(default=None, ge=1, le=6)
    course_type: CourseTypeLiteral | None = None


class CourseResponse(BaseModel):
    id: str
    department_id: str
    name: str
    code: str
    credits: int
    course_type: str

    model_config = {"from_attributes": True}


# Assessment
class AssessmentCreate(BaseModel):
    course_id: str
    name: str = Field(..., min_length=1, max_length=255)
    assessment_type: str = Field(..., pattern="^(CA|MID|FINAL|ASSIGNMENT)$")
    max_marks: float = Field(default=100.0, ge=0, le=100)
    date: DateType | None = None


class AssessmentUpdate(BaseModel):
    name: str | None = None
    assessment_type: str | None = Field(default=None, pattern="^(CA|MID|FINAL|ASSIGNMENT)$")
    max_marks: float | None = Field(default=None, ge=0, le=100)
    date: DateType | None = None


class AssessmentResponse(BaseModel):
    id: str
    course_id: str
    name: str
    assessment_type: str
    max_marks: float
    date: DateType | None = None

    model_config = {"from_attributes": True}


# Assessment Mark
class AssessmentMarkCreate(BaseModel):
    enrollment_id: str
    assessment_id: str
    marks_obtained: float = Field(..., ge=0, le=100)


class AssessmentMarkUpdate(BaseModel):
    marks_obtained: float = Field(..., ge=0, le=100)


class AssessmentMarkResponse(BaseModel):
    id: str
    enrollment_id: str
    assessment_id: str
    marks_obtained: float

    model_config = {"from_attributes": True}


# Attendance
class AttendanceCreate(BaseModel):
    enrollment_id: str
    date: DateType
    status: str = Field(..., pattern="^(present|absent)$")


class AttendanceUpdate(BaseModel):
    status: str = Field(..., pattern="^(present|absent)$")


class AttendanceResponse(BaseModel):
    id: str
    enrollment_id: str
    date: DateType
    status: str

    model_config = {"from_attributes": True}


# Enrollment
class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str
    semester_id: str
    section_id: str | None = None
    attendance_percentage: float | None = Field(default=None, ge=0, le=100)
    study_hours_per_week: float | None = Field(default=None, ge=0, le=60)
    assignment_completion_pct: float | None = Field(default=None, ge=0, le=100)


class EnrollmentUpdate(BaseModel):
    section_id: str | None = None
    attendance_percentage: float | None = Field(default=None, ge=0, le=100)
    study_hours_per_week: float | None = Field(default=None, ge=0, le=60)
    assignment_completion_pct: float | None = Field(default=None, ge=0, le=100)


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    semester_id: str
    section_id: str | None = None
    attendance_percentage: float | None = None
    study_hours_per_week: float | None = None
    assignment_completion_pct: float | None = None

    model_config = {"from_attributes": True}


# Course Result
class CourseResultCreate(BaseModel):
    enrollment_id: str
    grade: str | None = None
    end_marks: float | None = Field(default=None, ge=0, le=100)
    status: str = Field(default="PASS", pattern="^(PASS|FAIL)$")


class CourseResultUpdate(BaseModel):
    grade: str | None = None
    end_marks: float | None = Field(default=None, ge=0, le=100)
    status: str | None = Field(default=None, pattern="^(PASS|FAIL)$")


class CourseResultResponse(BaseModel):
    id: str
    enrollment_id: str
    grade: str | None = None
    end_marks: float | None = None
    status: str

    model_config = {"from_attributes": True}


# Semester Result
class SemesterResultCreate(BaseModel):
    student_id: str
    semester_id: str
    sgpa: float | None = Field(default=None, ge=0, le=10)
    cgpa: float | None = Field(default=None, ge=0, le=10)
    backlog_count: int = Field(default=0, ge=0)
    current_failed_courses: int = Field(default=0, ge=0)
    low_performance_course_count: int = Field(default=0, ge=0)
    performance_trend: str = Field(default="STABLE", pattern="^(DECLINING|STABLE|IMPROVING)$")


class SemesterResultUpdate(BaseModel):
    sgpa: float | None = Field(default=None, ge=0, le=10)
    cgpa: float | None = Field(default=None, ge=0, le=10)
    backlog_count: int | None = Field(default=None, ge=0)
    current_failed_courses: int | None = Field(default=None, ge=0)
    low_performance_course_count: int | None = Field(default=None, ge=0)
    performance_trend: str | None = Field(default=None, pattern="^(DECLINING|STABLE|IMPROVING)$")


class SemesterResultResponse(BaseModel):
    id: str
    student_id: str
    student_name: str | None = None
    roll_number: str | None = None
    semester_id: str
    sgpa: float | None = None
    cgpa: float | None = None
    backlog_count: int
    current_failed_courses: int
    low_performance_course_count: int
    performance_trend: str

    model_config = {"from_attributes": True}


# At-risk
class AtRiskStudentResponse(BaseModel):
    student_id: str
    student_name: str
    roll_number: str
    risk_score: float
    risk_level: str
    risk_factors: list[str] = []
    recommendations: list[str] = []
    predicted_at: datetime | None = None
    department_name: str | None = None
    program_name: str | None = None
    semester_number: int | None = None
    year_number: int | None = None
    attendance_percentage: float | None = None
    cgpa: float | None = None
    backlog_count: int | None = None
    performance_trend: str | None = None


# Bulk data entry
class BulkMarkEntry(BaseModel):
    enrollment_id: str
    assessment_id: str
    marks_obtained: float = Field(..., ge=0, le=100)


class BulkMarksRequest(BaseModel):
    entries: list[BulkMarkEntry] = Field(..., min_length=1)


class BulkAttendanceEntry(BaseModel):
    enrollment_id: str
    attendance_percentage: float = Field(..., ge=0, le=100)


class BulkAttendanceRequest(BaseModel):
    entries: list[BulkAttendanceEntry] = Field(..., min_length=1)


class RosterStudentRow(BaseModel):
    enrollment_id: str
    student_id: str
    student_name: str
    roll_number: str
    attendance_percentage: float | None = None
    mark_id: str | None = None
    marks_obtained: float | None = None
    end_marks: float | None = None
    course_result_status: str | None = None


class MarksRosterResponse(BaseModel):
    assessment_id: str
    assessment_name: str
    max_marks: float
    students: list[RosterStudentRow]


class AssessmentColumn(BaseModel):
    id: str
    name: str
    assessment_type: str
    max_marks: float


class MarkCell(BaseModel):
    assessment_id: str
    mark_id: str | None = None
    marks_obtained: float | None = None


class MarksGridStudentRow(BaseModel):
    enrollment_id: str
    student_id: str
    student_name: str
    roll_number: str
    section: str | None = None
    section_id: str | None = None
    attendance_percentage: float | None = None
    marks: list[MarkCell]
    total_marks: float | None = None
    grade: str | None = None
    status: str | None = None


class MarksGridResponse(BaseModel):
    course_id: str
    course_name: str
    course_code: str
    course_type: str
    assessments: list[AssessmentColumn]
    students: list[MarksGridStudentRow]


class AttendanceRosterRow(BaseModel):
    enrollment_id: str | None = None
    student_id: str
    student_name: str
    roll_number: str
    section: str | None = None
    # Stored enrollment percentage used by reports and ML. Not a date-range figure.
    attendance_percentage: float | None = None
    range_present: int | None = None
    range_absent: int | None = None
    # Present / (present + absent) inside the selected dates. Omitted without a date window.
    range_percentage: float | None = None


class AttendanceRosterResponse(BaseModel):
    course_id: str | None = None
    course_name: str | None = None
    course_code: str | None = None
    date_from: DateType | None = None
    date_to: DateType | None = None
    status: str | None = None
    students: list[AttendanceRosterRow]


class BulkMarkEntryNullable(BaseModel):
    enrollment_id: str
    assessment_id: str
    marks_obtained: float | None = None


class BulkMarksGridRequest(BaseModel):
    entries: list[BulkMarkEntryNullable] = Field(..., min_length=1)
    recalculate_results: bool = True
    trigger_predictions: bool = False


class CoursePerformanceRow(BaseModel):
    course_id: str
    course_name: str
    course_code: str
    credits: int
    marks: float | None = None
    grade: str | None = None
    grade_point: float | None = None
    status: str | None = None
    attendance_percentage: float | None = None


class SemesterPerformanceDetail(BaseModel):
    semester_id: str
    semester_number: int
    semester_name: str
    sgpa: float | None = None
    cgpa: float | None = None
    average_marks: float | None = None
    average_attendance: float | None = None
    passed_courses: int = 0
    failed_courses: int = 0
    backlogs: int = 0
    strongest_course: str | None = None
    weakest_course: str | None = None
    courses: list[CoursePerformanceRow] = []


class StudentPerformanceResponse(BaseModel):
    student_id: str
    student_name: str
    roll_number: str
    current_cgpa: float | None = None
    current_sgpa: float | None = None
    total_credits: int = 0
    backlogs: int = 0
    semesters: list[SemesterPerformanceDetail] = []


class GoalGuidanceResponse(BaseModel):
    current_cgpa: float | None = None
    target_cgpa: float | None = None
    recent_sgpa: list[float] = []
    predicted_performance: float | None = None
    required_sgpa_hint: float | None = None
    guidance: list[str] = []
