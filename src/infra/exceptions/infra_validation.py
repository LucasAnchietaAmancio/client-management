from src.shared.errors.app_error import AppError


class InfraValidation(AppError):
    def __init__(self,message: str,tag: str = "INFRASTRUCTURE_VALIDATION",external_error: Exception | None = None) -> None:
        self.external_error = external_error
        super().__init__(
            message=message,
            code=tag,
            category="INFRASTRUCTURE",
            error_type="UNAVAILABLE",
        )
