import unittest
from decimal import Decimal

from lms.assignments.models import Assignment
from lms.grading.adapter import LegacyGradeAdapter
from lms.grading.service import GradingService
from lms.grading.strategies import PassFailStrategy, PercentageStrategy
from lms.users.models import Instructor, Learner


class FakeLegacyEngine:
    def calculate_gpa(self, points_earned: Decimal, points_possible: Decimal) -> Decimal:
        return (points_earned / points_possible) * Decimal("4")


class GradingTests(unittest.TestCase):
    def published_assignment(self) -> Assignment:
        assignment = Assignment("a1", "c1", "Practice")
        assignment.publish()
        assignment.submit("answer")
        return assignment

    def test_percentage_strategy_grades_submitted_assignment(self) -> None:
        assignment = self.published_assignment()
        grade = GradingService(PercentageStrategy()).grade(
            Instructor("i1", "Avery", "avery@example.test"),
            assignment,
            "l1",
            Decimal("18"),
            Decimal("20"),
        )
        self.assertEqual(grade.percentage, Decimal("90.00"))
        self.assertEqual(assignment.state, "graded")

    def test_pass_fail_strategy_applies_threshold(self) -> None:
        strategy = PassFailStrategy(Decimal("70"))
        self.assertEqual(strategy.grade_percentage(Decimal("14"), Decimal("20")), Decimal("100.00"))
        self.assertEqual(strategy.grade_percentage(Decimal("13"), Decimal("20")), Decimal("0.00"))

    def test_legacy_adapter_converts_four_point_gpa_to_percentage(self) -> None:
        adapter = LegacyGradeAdapter(FakeLegacyEngine())
        self.assertEqual(adapter.grade_percentage(Decimal("3"), Decimal("4")), Decimal("75.00"))

    def test_percentage_strategy_rejects_invalid_scores(self) -> None:
        with self.assertRaises(ValueError):
            PercentageStrategy().grade_percentage(Decimal("21"), Decimal("20"))

    def test_grading_requires_a_submission(self) -> None:
        assignment = Assignment("a1", "c1", "Practice")
        with self.assertRaisesRegex(RuntimeError, "draft state"):
            GradingService(PercentageStrategy()).grade(
                Instructor("i1", "Avery", "avery@example.test"),
                assignment,
                "l1",
                Decimal("18"),
                Decimal("20"),
            )

    def test_only_instructors_can_grade(self) -> None:
        assignment = self.published_assignment()
        with self.assertRaises(PermissionError):
            GradingService(PercentageStrategy()).grade(
                Learner("l1", "Sam", "sam@example.test"),
                assignment,
                "l1",
                Decimal("18"),
                Decimal("20"),
            )  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
