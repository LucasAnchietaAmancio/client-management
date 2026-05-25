from domain.exceptions.domain_validation_error import DomainValidationError

class EmptyValueError(DomainValidationError):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="EMPTY_VALUE",
        )
