"""Run a compact end-to-end LMS demonstration with `python -m lms`."""

from decimal import Decimal

from lms.assignments.models import Assignment
from lms.assignments.service import AssignmentService, AssignmentSubmitted
from lms.core.events import EventBus
from lms.courses.models import CourseBuilder
from lms.courses.repository import InMemoryCourseRepository
from lms.courses.service import CourseService
from lms.grading.service import GradingService
from lms.grading.strategies import PercentageStrategy
from lms.notifications.channels import ConsoleDeliveryGateway, EmailChannel, InAppChannel
from lms.notifications.factory import NotificationFactory
from lms.notifications.observers import AssignmentSubmittedNotifier
from lms.reports.service import ReportService
from lms.users.models import Instructor, Learner
from lms.users.repository import InMemoryUserRepository
from lms.users.service import UserService


def main() -> None:
    users = UserService(InMemoryUserRepository())
    instructor = users.register(Instructor("instructor-1", "Avery Chen", "avery@example.test"))
    learner = users.register(Learner("learner-1", "Sam Rivera", "sam@example.test"))

    course_repository = InMemoryCourseRepository()
    course_service = CourseService(course_repository)
    course = course_service.create_course(
        CourseBuilder("course-101", "Python Foundations", instructor.id)
        .with_description("Core Python concepts and practical exercises")
        .add_module("Objects and classes", "Encapsulation, inheritance, and composition")
        .add_module("Testing", "Unit testing with the standard library")
    )
    course_service.enroll(course.id, learner)

    events = EventBus()
    gateway = ConsoleDeliveryGateway()
    notification_factory = NotificationFactory(
        {"email": EmailChannel(gateway), "in-app": InAppChannel(gateway)}
    )
    notifier = AssignmentSubmittedNotifier(notification_factory)
    events.subscribe(AssignmentSubmitted, notifier.on_assignment_submitted)

    assignment = Assignment("assignment-1", course.id, "Model a library")
    assignment_service = AssignmentService(events)
    assignment_service.publish(instructor, assignment)
    assignment_service.submit(learner, assignment, "I used entities, repositories, and tests.")

    grade = GradingService(PercentageStrategy()).grade(
        instructor, assignment, learner.id, Decimal("18"), Decimal("20")
    )
    summary = ReportService(course_repository).course_summary()
    print(f"Grade: {grade.percentage}% ({assignment.state})")
    print(
        f"Report: {summary.course_count} course(s), "
        f"{summary.learner_enrollment_count} enrollment(s): {', '.join(summary.course_titles)}"
    )


if __name__ == "__main__":
    main()
