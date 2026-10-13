"""Course catalog summary report."""

from dataclasses import dataclass

from lms.courses.repository import CourseRepository


@dataclass(frozen=True)
class CourseSummary:
    course_count: int
    learner_enrollment_count: int
    course_titles: tuple[str, ...]


class ReportService:
    def __init__(self, courses: CourseRepository) -> None:
        self._courses = courses

    def course_summary(self) -> CourseSummary:
        courses = self._courses.list_all()
        return CourseSummary(
            course_count=len(courses),
            learner_enrollment_count=sum(len(course.learner_ids) for course in courses),
            course_titles=tuple(course.title for course in courses),
        )
