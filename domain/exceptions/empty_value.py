from .domain_validation import DomainValidation

class EmptyValue(DomainValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="EMPTY_VALUE",
        )
