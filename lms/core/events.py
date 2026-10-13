"""A small thread-safe in-process Observer/event bus."""

from collections import defaultdict
from threading import RLock
from typing import Callable, TypeVar, cast

Event = TypeVar("Event")
Handler = Callable[[object], None]


class EventBus:
    """Subscribe handlers by event type and publish without holding the registry lock."""

    def __init__(self) -> None:
        self._handlers: dict[type[object], list[Handler]] = defaultdict(list)
        self._lock = RLock()

    def subscribe(self, event_type: type[Event], handler: Callable[[Event], None]) -> Callable[[], None]:
        erased_handler = cast(Handler, handler)
        with self._lock:
            self._handlers[event_type].append(erased_handler)

        def unsubscribe() -> None:
            with self._lock:
                handlers = self._handlers.get(event_type, [])
                if erased_handler in handlers:
                    handlers.remove(erased_handler)

        return unsubscribe

    def publish(self, event: object) -> None:
        with self._lock:
            handlers = tuple(self._handlers.get(type(event), ()))
        for handler in handlers:
            handler(event)
