"""Grading use case and immutable grade report."""

from dataclasses import dataclass
from decimal import Decimal

from lms.assignments.models import Assignment
from lms.assignments.security import require_role
from lms.grading.strategies import GradingStrategy
from lms.users.models import Instructor, Role


@dataclass(frozen=True)
class GradeRecord:
    assignment_id: str
    learner_id: str
    points_earned: Decimal
    points_possible: Decimal
    percentage: Decimal


class GradingService:
    def __init__(self, strategy: GradingStrategy) -> None:
        self._strategy = strategy

    @require_role(Role.INSTRUCTOR)
    def grade(
        self,
        actor: Instructor,
        assignment: Assignment,
        learner_id: str,
        points_earned: Decimal,
        points_possible: Decimal,
    ) -> GradeRecord:
        percentage = self._strategy.grade_percentage(points_earned, points_possible)
        assignment.record_grade(percentage)
        return GradeRecord(
            assignment_id=assignment.id,
            learner_id=learner_id,
            points_earned=points_earned,
            points_possible=points_possible,
            percentage=percentage,
        )
