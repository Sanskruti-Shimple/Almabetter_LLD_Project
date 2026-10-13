"""Course application service, independent of its persistence mechanism."""

from lms.courses.models import Course, CourseBuilder
from lms.courses.repository import CourseRepository
from lms.users.models import Learner


class CourseService:
    def __init__(self, courses: CourseRepository) -> None:
        self._courses = courses

    def create_course(self, builder: CourseBuilder) -> Course:
        course = builder.build()
        self._courses.add(course)
        return course

    def enroll(self, course_id: str, learner: Learner) -> Course:
        course = self._courses.get(course_id)
        enrolled_course = course.enroll(learner.id)
        self._courses.update(enrolled_course)
        return enrolled_course
