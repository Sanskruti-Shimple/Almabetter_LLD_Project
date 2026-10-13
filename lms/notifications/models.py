"""Transport-independent notification value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    recipient: str
    subject: str
    body: str
