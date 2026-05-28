from typing import Any
from src.shared.errors.app_error import AppError

class EventAlreadyProcessed(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="EVENT_ALREADY_PROCESSED",
            category="CONFLICT",
            message=message,
            external_error=external_error,
        )
