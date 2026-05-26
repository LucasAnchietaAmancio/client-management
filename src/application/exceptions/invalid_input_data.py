from .application_validation import ApplicationValidation

class InvalidInputData(ApplicationValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="INVALID_INPUT_DATA",
        )
