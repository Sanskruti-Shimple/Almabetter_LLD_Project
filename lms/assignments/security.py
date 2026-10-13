"""Role-based access-control decorator for application-service methods."""

from functools import wraps
from typing import Callable, ParamSpec, TypeVar

from lms.users.models import Role, User

P = ParamSpec("P")
R = TypeVar("R")


def require_role(required_role: Role) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(method: Callable[P, R]) -> Callable[P, R]:
        @wraps(method)
        def authorized(*args: P.args, **kwargs: P.kwargs) -> R:
            actor = kwargs.get("actor")
            if actor is None and len(args) > 1:
                actor = args[1]
            if not isinstance(actor, User) or actor.role is not required_role:
                raise PermissionError(f"This action requires the {required_role.value} role")
            return method(*args, **kwargs)

        return authorized

    return decorator
