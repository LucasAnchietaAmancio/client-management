
from src.shared.errors.app_error import AppError

class DomainValidation(AppError):
    def __init__(self,message: str,tag: str = "DOMAIN_VALIDATION") -> None:
        super().__init__(
            message=message,
            code=tag,
            category="DOMAIN",
            error_type="VALIDATION",
        )
