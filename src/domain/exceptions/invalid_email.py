from typing import Any
from src.shared.errors.app_error import AppError

class InvalidEmail(AppError):
    def __init__(self,message: str = "Invalid email",external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="INVALID_EMAIL",
            category="VALIDATION",
            message=message,
            external_error=external_error,
        )
