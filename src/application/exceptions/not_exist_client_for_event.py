from typing import Any
from src.shared.errors.app_error import AppError

class NotExistClientForEvent(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="NOT_EXIST_CLIENT_FOR_EVENT",
            category="NOT_FOUND",
            message=message,
            external_error=external_error,
        )
