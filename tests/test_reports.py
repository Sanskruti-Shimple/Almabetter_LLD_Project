import unittest

from lms.courses.models import CourseBuilder
from lms.courses.repository import InMemoryCourseRepository
from lms.courses.service import CourseService
from lms.reports.service import ReportService
from lms.users.models import Learner


class ReportTests(unittest.TestCase):
    def test_course_summary_counts_courses_and_enrollments(self) -> None:
        repository = InMemoryCourseRepository()
        service = CourseService(repository)
        course = service.create_course(CourseBuilder("c1", "Python", "i1"))
        service.enroll(course.id, Learner("l1", "Sam", "sam@example.test"))
        summary = ReportService(repository).course_summary()
        self.assertEqual(summary.course_count, 1)
        self.assertEqual(summary.learner_enrollment_count, 1)
        self.assertEqual(summary.course_titles, ("Python",))


if __name__ == "__main__":
    unittest.main()
