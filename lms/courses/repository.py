"""Course repository contract and thread-safe in-memory adapter."""

from threading import RLock
from typing import Protocol

from lms.courses.models import Course


class CourseRepository(Protocol):
    def add(self, course: Course) -> None: ...

    def get(self, course_id: str) -> Course: ...

    def list_all(self) -> tuple[Course, ...]: ...

    def update(self, course: Course) -> None: ...


class InMemoryCourseRepository:
    def __init__(self) -> None:
        self._courses: dict[str, Course] = {}
        self._lock = RLock()

    def add(self, course: Course) -> None:
        with self._lock:
            if course.id in self._courses:
                raise ValueError(f"Course already exists: {course.id}")
            self._courses[course.id] = course

    def get(self, course_id: str) -> Course:
        with self._lock:
            try:
                return self._courses[course_id]
            except KeyError as error:
                raise KeyError(f"Unknown course: {course_id}") from error

    def list_all(self) -> tuple[Course, ...]:
        with self._lock:
            return tuple(self._courses.values())

    def update(self, course: Course) -> None:
        with self._lock:
            if course.id not in self._courses:
                raise KeyError(f"Unknown course: {course.id}")
            self._courses[course.id] = course
