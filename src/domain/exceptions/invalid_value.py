from .domain_validation import DomainValidation

class InvalidValue(DomainValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="INVALID_VALUE",
        )
