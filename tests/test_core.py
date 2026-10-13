import unittest

from lms.core.events import EventBus
from lms.core.settings import LMSSettings
from lms.users.models import Learner
from lms.users.repository import InMemoryUserRepository
from lms.users.service import UserService


class CoreTests(unittest.TestCase):
    def test_settings_is_a_process_singleton(self) -> None:
        self.assertIs(LMSSettings(), LMSSettings())

    def test_event_bus_unsubscribe_stops_future_delivery(self) -> None:
        events = EventBus()
        received: list[str] = []
        unsubscribe = events.subscribe(str, received.append)
        events.publish("first")
        unsubscribe()
        events.publish("second")
        self.assertEqual(received, ["first"])

    def test_user_service_registers_and_retrieves_a_user(self) -> None:
        service = UserService(InMemoryUserRepository())
        learner = Learner("l1", "Sam", "sam@example.test")
        service.register(learner)
        self.assertEqual(service.get(learner.id), learner)


if __name__ == "__main__":
    unittest.main()
