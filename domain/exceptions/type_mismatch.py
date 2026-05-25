from domain.exceptions.domain_validation_error import DomainValidationError

class TypeMismatch(DomainValidationError):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="TYPE_MISMATCH",
        )
