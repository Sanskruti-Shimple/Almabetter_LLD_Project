"""Pluggable grading algorithms."""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


class GradingStrategy(ABC):
    @abstractmethod
    def grade_percentage(self, points_earned: Decimal, points_possible: Decimal) -> Decimal:
        """Convert a score into a percentage from 0 through 100."""


class PercentageStrategy(GradingStrategy):
    def grade_percentage(self, points_earned: Decimal, points_possible: Decimal) -> Decimal:
        if points_possible <= 0:
            raise ValueError("points_possible must be greater than zero")
        if points_earned < 0 or points_earned > points_possible:
            raise ValueError("points_earned must be between zero and points_possible")
        return ((points_earned / points_possible) * Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


class PassFailStrategy(GradingStrategy):
    def __init__(self, passing_percentage: Decimal = Decimal("60")) -> None:
        if not Decimal("0") <= passing_percentage <= Decimal("100"):
            raise ValueError("passing_percentage must be between 0 and 100")
        self._passing_percentage = passing_percentage
        self._percentage = PercentageStrategy()

    def grade_percentage(self, points_earned: Decimal, points_possible: Decimal) -> Decimal:
        percentage = self._percentage.grade_percentage(points_earned, points_possible)
        return Decimal("100.00") if percentage >= self._passing_percentage else Decimal("0.00")
