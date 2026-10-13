"""User repository contract and in-memory implementation."""

from threading import RLock
from typing import Protocol

from lms.users.models import User


class UserRepository(Protocol):
    def add(self, user: User) -> None: ...

    def get(self, user_id: str) -> User: ...


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._lock = RLock()

    def add(self, user: User) -> None:
        with self._lock:
            if user.id in self._users:
                raise ValueError(f"User already exists: {user.id}")
            self._users[user.id] = user

    def get(self, user_id: str) -> User:
        with self._lock:
            try:
                return self._users[user_id]
            except KeyError as error:
                raise KeyError(f"Unknown user: {user_id}") from error
