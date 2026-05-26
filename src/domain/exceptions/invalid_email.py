from .domain_validation import DomainValidation

class InvalidEmail(DomainValidation):
    def __init__(self,message: str = "Invalid email") -> None:
        super().__init__(
            message=message,
            tag="INVALID_EMAIL",
        )
