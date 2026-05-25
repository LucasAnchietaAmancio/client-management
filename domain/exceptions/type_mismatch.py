from domain.exceptions.domain_validation import DomainValidation


class TypeMismatch(DomainValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="TYPE_MISMATCH",
        )
