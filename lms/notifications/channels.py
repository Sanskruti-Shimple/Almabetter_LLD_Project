"""Notification Bridge implementations and a legacy SMS Adapter."""

from abc import ABC, abstractmethod
from threading import RLock
from typing import Protocol

from lms.notifications.models import Notification


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, notification: Notification) -> None:
        """Deliver a notification through a concrete channel."""


class DeliveryGateway(Protocol):
    def deliver(self, channel: str, notification: Notification) -> None: ...


class ConsoleDeliveryGateway:
    def deliver(self, channel: str, notification: Notification) -> None:
        print(f"[{channel}] To: {notification.recipient} | {notification.subject}: {notification.body}")


class MemoryDeliveryGateway:
    """Useful for tests and local demos; production adapters can implement DeliveryGateway."""

    def __init__(self) -> None:
        self.deliveries: list[tuple[str, Notification]] = []
        self._lock = RLock()

    def deliver(self, channel: str, notification: Notification) -> None:
        with self._lock:
            self.deliveries.append((channel, notification))


class EmailChannel(NotificationChannel):
    def __init__(self, gateway: DeliveryGateway) -> None:
        self._gateway = gateway

    def send(self, notification: Notification) -> None:
        self._gateway.deliver("email", notification)


class InAppChannel(NotificationChannel):
    def __init__(self, gateway: DeliveryGateway) -> None:
        self._gateway = gateway

    def send(self, notification: Notification) -> None:
        self._gateway.deliver("in-app", notification)


class LegacySmsGateway(Protocol):
    def send_text(self, phone_number: str, message: str) -> None: ...


class LegacySmsChannelAdapter(NotificationChannel):
    """Adapts an older SMS API to the LMS NotificationChannel interface."""

    def __init__(self, legacy_gateway: LegacySmsGateway) -> None:
        self._legacy_gateway = legacy_gateway

    def send(self, notification: Notification) -> None:
        self._legacy_gateway.send_text(
            notification.recipient,
            f"{notification.subject}: {notification.body}",
        )
