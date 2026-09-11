"""Academic entity request/response schemas."""

from datetime import date as DateType
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


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


# Faculty
class FacultyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    department_id: str


class FacultyUpdate(BaseModel):
    name: str | None = None
    department_id: str | None = None


class FacultyResponse(BaseModel):
    id: str
    name: str
    email: str | None = None
    department_id: str
    user_id: str

    model_config = {"from_attributes": True}


# Parent
class ParentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    student_ids: list[str] = Field(default_factory=list)


class ParentUpdate(BaseModel):
    name: str | None = None


class ParentResponse(BaseModel):
    id: str
    name: str
    user_id: str
    linked_student_ids: list[str] = []

    model_config = {"from_attributes": True}


# Student
class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    roll_number: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6)
    department_id: str
    program_id: str | None = None
    semester: int = Field(default=1, ge=1, le=8)
    branch: str = Field(default="CSE", max_length=50)


class StudentUpdate(BaseModel):
    name: str | None = None
    department_id: str | None = None
    program_id: str | None = None
    semester: int | None = Field(default=None, ge=1, le=8)
    branch: str | None = None


class StudentResponse(BaseModel):
    id: str
    roll_number: str
    name: str
    department_id: str
    program_id: str | None = None
    semester: int
    branch: str
    section: str | None = None

    model_config = {"from_attributes": True}


# Course
class CourseCreate(BaseModel):
    department_id: str
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    credits: int = Field(default=3, ge=1, le=6)
    course_type: str = Field(default="THEORY", max_length=50)


class CourseUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    credits: int | None = Field(default=None, ge=1, le=6)
    course_type: str | None = None


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
    attendance_percentage: float | None = Field(default=None, ge=0, le=100)
    study_hours_per_week: float | None = Field(default=None, ge=0, le=60)
    assignment_completion_pct: float | None = Field(default=None, ge=0, le=100)


class EnrollmentUpdate(BaseModel):
    attendance_percentage: float | None = Field(default=None, ge=0, le=100)
    study_hours_per_week: float | None = Field(default=None, ge=0, le=60)
    assignment_completion_pct: float | None = Field(default=None, ge=0, le=100)


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    course_id: str
    semester_id: str
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
    semester: int | None = None
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
    enrollment_id: str
    student_id: str
    student_name: str
    roll_number: str
    section: str | None = None
    attendance_percentage: float | None = None


class AttendanceRosterResponse(BaseModel):
    course_id: str
    course_name: str
    course_code: str
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
