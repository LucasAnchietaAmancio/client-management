from typing import Any
from src.shared.errors.app_error import AppError

class InvalidInputData(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="INVALID_INPUT_DATA",
            category="INPUT",
            message=message,
            external_error=external_error,
        )
