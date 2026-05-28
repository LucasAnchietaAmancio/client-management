from typing import Any
from src.shared.errors.app_error import AppError

class FailPersistOnDatabase(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="FAIL_PERSIST",
            category="UNAVAILABLE",
            message=message,
            external_error=external_error,
        )
