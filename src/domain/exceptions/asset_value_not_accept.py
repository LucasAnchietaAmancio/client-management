from typing import Any
from src.shared.errors.app_error import AppError

class AssetValueNotAccept(AppError):
    def __init__(self,message: str,external_error: Exception | Any = None) -> None:
        super().__init__(
            tag="ASSET_VALUE_NOT_ACCEPT",
            category="VALIDATION",
            message=message,
            external_error=external_error,
        )
