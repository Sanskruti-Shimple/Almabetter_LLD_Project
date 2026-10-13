"""Assignment aggregate with atomic state transitions."""

from dataclasses import dataclass, field
from decimal import Decimal
from threading import RLock

from lms.assignments.states import AssignmentState, DraftState


@dataclass
class Assignment:
    id: str
    course_id: str
    title: str
    _state: AssignmentState = field(default_factory=DraftState, repr=False)
    submission_text: str | None = None
    final_percentage: Decimal | None = None
    _lock: RLock = field(default_factory=RLock, init=False, repr=False, compare=False)

    @property
    def state(self) -> str:
        with self._lock:
            return self._state.name

    def publish(self) -> None:
        with self._lock:
            self._state.publish(self)

    def submit(self, text: str) -> None:
        with self._lock:
            self._state.submit(self, text)

    def record_grade(self, percentage: Decimal) -> None:
        with self._lock:
            self._state.grade(self, percentage)

    def _set_state(self, state: AssignmentState) -> None:
        self._state = state
