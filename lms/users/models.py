"""User roles and domain entities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    LEARNER = "learner"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


@dataclass(frozen=True)
class User(ABC):
    id: str
    name: str
    email: str

    @property
    @abstractmethod
    def role(self) -> Role:
        """Return the concrete user's authorization role."""


@dataclass(frozen=True)
class Learner(User):
    @property
    def role(self) -> Role:
        return Role.LEARNER


@dataclass(frozen=True)
class Instructor(User):
    @property
    def role(self) -> Role:
        return Role.INSTRUCTOR


@dataclass(frozen=True)
class Administrator(User):
    @property
    def role(self) -> Role:
        return Role.ADMIN
