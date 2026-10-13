"""Assignment use cases and their domain events."""

from dataclasses import dataclass

from lms.assignments.models import Assignment
from lms.assignments.security import require_role
from lms.core.events import EventBus
from lms.users.models import Instructor, Learner, Role


@dataclass(frozen=True)
class AssignmentSubmitted:
    assignment_id: str
    assignment_title: str
    learner_id: str
    learner_email: str


class AssignmentService:
    def __init__(self, events: EventBus) -> None:
        self._events = events

    @require_role(Role.INSTRUCTOR)
    def publish(self, actor: Instructor, assignment: Assignment) -> None:
        assignment.publish()

    @require_role(Role.LEARNER)
    def submit(self, actor: Learner, assignment: Assignment, text: str) -> None:
        assignment.submit(text)
        self._events.publish(
            AssignmentSubmitted(
                assignment_id=assignment.id,
                assignment_title=assignment.title,
                learner_id=actor.id,
                learner_email=actor.email,
            )
        )
