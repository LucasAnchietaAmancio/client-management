from typing import Any
from src.shared.errors.app_error import AppError

class FailPipefyRequest(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="FAIL_PIPEFY_REQUEST",
            category="UNAVAILABLE",
            message=message,
            external_error=external_error,
        )
