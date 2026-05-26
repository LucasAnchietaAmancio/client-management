from .infra_validation import InfraValidation

class FailSearchOnDatabase(InfraValidation):
    def __init__(self,message: str,external_error: Exception | None) -> None:
        super().__init__(
            message=message,
            tag="FAIL_SEARCH",
            external_error=external_error,
        )
