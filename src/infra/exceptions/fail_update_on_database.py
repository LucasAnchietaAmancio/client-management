from .infra_validation import InfraValidation

class FailUpdateOnDatabase(InfraValidation):
    def __init__(self,message: str,external_error: Exception | None) -> None:
        super().__init__(
            message=message,
            tag="FAIL_UPDATE",
            external_error=external_error,
        )
