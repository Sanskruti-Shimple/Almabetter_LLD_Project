"""Adapter that makes a legacy 4-point grade engine satisfy GradingStrategy."""

from decimal import Decimal, ROUND_HALF_UP
from typing import Protocol

from lms.grading.strategies import GradingStrategy


class LegacyGradeEngine(Protocol):
    def calculate_gpa(self, points_earned: Decimal, points_possible: Decimal) -> Decimal: ...


class LegacyGradeAdapter(GradingStrategy):
    def __init__(self, legacy_engine: LegacyGradeEngine) -> None:
        self._legacy_engine = legacy_engine

    def grade_percentage(self, points_earned: Decimal, points_possible: Decimal) -> Decimal:
        gpa = self._legacy_engine.calculate_gpa(points_earned, points_possible)
        if not Decimal("0") <= gpa <= Decimal("4"):
            raise ValueError("Legacy GPA must be between 0 and 4")
        return ((gpa / Decimal("4")) * Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
