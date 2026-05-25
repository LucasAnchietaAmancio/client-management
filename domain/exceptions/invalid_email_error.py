from domain.exceptions.domain_validation_error import DomainValidationError

class InvalidEmailError(DomainValidationError):
    def __init__(self,message: str = "Invalid email") -> None:
        super().__init__(
            message=message,
            tag="INVALID_EMAIL",
        )
