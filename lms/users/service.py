"""User registration and lookup use cases."""

from lms.users.models import User
from lms.users.repository import UserRepository


class UserService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def register(self, user: User) -> User:
        self._users.add(user)
        return user

    def get(self, user_id: str) -> User:
        return self._users.get(user_id)
