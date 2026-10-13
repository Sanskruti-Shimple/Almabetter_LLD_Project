import unittest

from lms.assignments.models import Assignment
from lms.assignments.service import AssignmentService, AssignmentSubmitted
from lms.core.events import EventBus
from lms.users.models import Instructor, Learner


class AssignmentLifecycleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.events = EventBus()
        self.service = AssignmentService(self.events)
        self.instructor = Instructor("i1", "Avery", "avery@example.test")
        self.learner = Learner("l1", "Sam", "sam@example.test")
        self.assignment = Assignment("a1", "c1", "Practice")

    def test_publish_submit_and_notify(self) -> None:
        received: list[AssignmentSubmitted] = []
        self.events.subscribe(AssignmentSubmitted, received.append)
        self.service.publish(self.instructor, self.assignment)
        self.service.submit(self.learner, self.assignment, "My answer")
        self.assertEqual(self.assignment.state, "submitted")
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].learner_email, self.learner.email)

    def test_only_instructor_can_publish(self) -> None:
        with self.assertRaises(PermissionError):
            self.service.publish(self.learner, self.assignment)  # type: ignore[arg-type]

    def test_only_learner_can_submit(self) -> None:
        with self.assertRaises(PermissionError):
            self.service.submit(self.instructor, self.assignment, "answer")  # type: ignore[arg-type]

    def test_cannot_submit_before_publish(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "draft state"):
            self.service.submit(self.learner, self.assignment, "answer")

    def test_assignment_rejects_empty_submission(self) -> None:
        self.service.publish(self.instructor, self.assignment)
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.service.submit(self.learner, self.assignment, "  ")


if __name__ == "__main__":
    unittest.main()
