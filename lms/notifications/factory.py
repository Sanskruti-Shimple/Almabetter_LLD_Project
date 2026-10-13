"""Factory for selecting a notification channel at runtime."""

from collections.abc import Mapping

from lms.notifications.channels import NotificationChannel
from lms.notifications.models import Notification


class NotificationSender:
    """Bridge abstraction: sender policy is independent of channel implementation."""

    def __init__(self, channel: NotificationChannel) -> None:
        self._channel = channel

    def send(self, notification: "Notification") -> None:
        self._channel.send(notification)


class NotificationFactory:
    def __init__(self, channels: Mapping[str, NotificationChannel]) -> None:
        self._channels = {name.lower(): channel for name, channel in channels.items()}

    def create_sender(self, channel_name: str) -> NotificationSender:
        try:
            return NotificationSender(self._channels[channel_name.lower()])
        except KeyError as error:
            raise ValueError(f"Unsupported notification channel: {channel_name}") from error
