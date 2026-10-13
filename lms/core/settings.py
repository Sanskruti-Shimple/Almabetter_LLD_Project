"""Process-wide immutable-by-convention application defaults."""

from threading import Lock


class LMSSettings:
    """Thread-safe Singleton for settings that are shared within one process."""

    _instance: "LMSSettings | None" = None
    _instance_lock = Lock()

    def __new__(cls) -> "LMSSettings":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self.default_timezone = "UTC"
        self._initialized = True
