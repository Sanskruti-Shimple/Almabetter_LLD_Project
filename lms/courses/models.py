"""Course entities and the fluent CourseBuilder."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class CourseModule:
    id: str
    title: str
    description: str


@dataclass(frozen=True)
class Course:
    id: str
    title: str
    instructor_id: str
    description: str
    modules: tuple[CourseModule, ...]
    learner_ids: frozenset[str] = frozenset()

    def enroll(self, learner_id: str) -> "Course":
        if not learner_id:
            raise ValueError("learner_id cannot be empty")
        return replace(self, learner_ids=self.learner_ids | {learner_id})


class CourseBuilder:
    """Builder keeps optional course construction details out of the domain constructor."""

    def __init__(self, course_id: str, title: str, instructor_id: str) -> None:
        self._course_id = course_id
        self._title = title
        self._instructor_id = instructor_id
        self._description = ""
        self._modules: list[CourseModule] = []

    def with_description(self, description: str) -> "CourseBuilder":
        self._description = description
        return self

    def add_module(self, title: str, description: str = "") -> "CourseBuilder":
        module_id = f"{self._course_id}-module-{len(self._modules) + 1}"
        self._modules.append(CourseModule(module_id, title, description))
        return self

    def build(self) -> Course:
        if not self._course_id.strip() or not self._title.strip() or not self._instructor_id.strip():
            raise ValueError("Course id, title, and instructor id are required")
        if any(not module.title.strip() for module in self._modules):
            raise ValueError("Every course module must have a title")
        return Course(
            id=self._course_id,
            title=self._title,
            instructor_id=self._instructor_id,
            description=self._description,
            modules=tuple(self._modules),
        )
