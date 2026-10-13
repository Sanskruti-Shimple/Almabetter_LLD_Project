import unittest

from lms.assignments.service import AssignmentSubmitted
from lms.core.events import EventBus
from lms.notifications.channels import (
    EmailChannel,
    LegacySmsChannelAdapter,
    MemoryDeliveryGateway,
)
from lms.notifications.factory import NotificationFactory
from lms.notifications.models import Notification
from lms.notifications.observers import AssignmentSubmittedNotifier


class FakeLegacySmsGateway:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send_text(self, phone_number: str, message: str) -> None:
        self.sent.append((phone_number, message))


class NotificationTests(unittest.TestCase):
    def test_factory_and_bridge_dispatch_to_selected_channel(self) -> None:
        gateway = MemoryDeliveryGateway()
        factory = NotificationFactory({"email": EmailChannel(gateway)})
        sender = factory.create_sender("EMAIL")
        sender.send(Notification("sam@example.test", "Hello", "Welcome"))
        self.assertEqual(gateway.deliveries[0][0], "email")

    def test_factory_rejects_unknown_channel(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported"):
            NotificationFactory({}).create_sender("fax")

    def test_legacy_sms_adapter_translates_call_shape(self) -> None:
        legacy = FakeLegacySmsGateway()
        channel = LegacySmsChannelAdapter(legacy)
        channel.send(Notification("+15550001111", "Due date", "Tomorrow"))
        self.assertEqual(legacy.sent, [("+15550001111", "Due date: Tomorrow")])

    def test_observer_sends_notification_for_submission_event(self) -> None:
        gateway = MemoryDeliveryGateway()
        factory = NotificationFactory({"email": EmailChannel(gateway)})
        notifier = AssignmentSubmittedNotifier(factory)
        events = EventBus()
        events.subscribe(AssignmentSubmitted, notifier.on_assignment_submitted)
        events.publish(AssignmentSubmitted("a1", "Practice", "l1", "sam@example.test"))
        self.assertEqual(len(gateway.deliveries), 1)
        self.assertIn("Practice", gateway.deliveries[0][1].body)


if __name__ == "__main__":
    unittest.main()
