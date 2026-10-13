import unittest

from lms.courses.models import CourseBuilder
from lms.courses.repository import InMemoryCourseRepository
from lms.courses.service import CourseService
from lms.users.models import Learner


class CourseManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryCourseRepository()
        self.service = CourseService(self.repository)
        self.learner = Learner("learner-1", "Sam Rivera", "sam@example.test")

    def test_builder_creates_course_and_optional_modules(self) -> None:
        course = self.service.create_course(
            CourseBuilder("course-1", "Python", "instructor-1")
            .with_description("A Python course")
            .add_module("Basics")
        )
        self.assertEqual(course.description, "A Python course")
        self.assertEqual(course.modules[0].title, "Basics")

    def test_enrollment_updates_immutable_course_record(self) -> None:
        course = self.service.create_course(CourseBuilder("course-1", "Python", "i1"))
        enrolled = self.service.enroll(course.id, self.learner)
        self.assertIn(self.learner.id, enrolled.learner_ids)
        self.assertEqual(self.repository.get(course.id), enrolled)
        self.assertNotIn(self.learner.id, course.learner_ids)

    def test_duplicate_course_is_rejected(self) -> None:
        builder = CourseBuilder("course-1", "Python", "i1")
        self.service.create_course(builder)
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.service.create_course(builder)

    def test_builder_rejects_missing_required_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "required"):
            CourseBuilder("", "Python", "i1").build()


if __name__ == "__main__":
    unittest.main()
