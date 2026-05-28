from typing import Any
from src.shared.errors.app_error import AppError

class InvalidValue(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="INVALID_VALUE",
            category="VALIDATION",
            message=message,
            external_error=external_error,
        )
