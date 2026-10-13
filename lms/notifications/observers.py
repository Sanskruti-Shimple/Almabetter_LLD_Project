"""Observer that reacts to assignment-submission events."""

from lms.assignments.service import AssignmentSubmitted
from lms.notifications.factory import NotificationFactory
from lms.notifications.models import Notification


class AssignmentSubmittedNotifier:
    def __init__(self, factory: NotificationFactory, channel_name: str = "email") -> None:
        self._sender = factory.create_sender(channel_name)

    def on_assignment_submitted(self, event: AssignmentSubmitted) -> None:
        self._sender.send(
            Notification(
                recipient=event.learner_email,
                subject="Submission received",
                body=f"Your submission for '{event.assignment_title}' was received.",
            )
        )
