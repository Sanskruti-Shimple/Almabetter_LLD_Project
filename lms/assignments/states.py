"""State objects constrain assignment lifecycle transitions."""

from abc import ABC
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lms.assignments.models import Assignment


class InvalidStateTransition(RuntimeError):
    pass


class AssignmentState(ABC):
    name = "unknown"

    def publish(self, assignment: "Assignment") -> None:
        raise InvalidStateTransition(f"Cannot publish an assignment in {self.name} state")

    def submit(self, assignment: "Assignment", text: str) -> None:
        raise InvalidStateTransition(f"Cannot submit an assignment in {self.name} state")

    def grade(self, assignment: "Assignment", percentage: Decimal) -> None:
        raise InvalidStateTransition(f"Cannot grade an assignment in {self.name} state")


class DraftState(AssignmentState):
    name = "draft"

    def publish(self, assignment: "Assignment") -> None:
        assignment._set_state(PublishedState())


class PublishedState(AssignmentState):
    name = "published"

    def submit(self, assignment: "Assignment", text: str) -> None:
        if not text.strip():
            raise ValueError("Submission text cannot be empty")
        assignment.submission_text = text
        assignment._set_state(SubmittedState())


class SubmittedState(AssignmentState):
    name = "submitted"

    def grade(self, assignment: "Assignment", percentage: Decimal) -> None:
        if not Decimal("0") <= percentage <= Decimal("100"):
            raise ValueError("Grade percentage must be between 0 and 100")
        assignment.final_percentage = percentage
        assignment._set_state(GradedState())


class GradedState(AssignmentState):
    name = "graded"
