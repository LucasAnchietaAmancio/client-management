from typing import Any
from src.shared.errors.app_error import AppError

class FailUpdateOnDatabase(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="FAIL_UPDATE",
            category="UNAVAILABLE",
            message=message,
            external_error=external_error,
        )
