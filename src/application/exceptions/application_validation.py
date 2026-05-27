
from src.shared.errors.app_error import AppError


class ApplicationValidation(AppError):
    def __init__(self,message: str,tag: str = "APPLICATION_VALIDATION",error_type: str = "VALIDATION") -> None:
        super().__init__(
            message=message,
            code=tag,
            category="APPLICATION",
            error_type=error_type,
        )
