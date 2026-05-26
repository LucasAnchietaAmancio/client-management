from .application_validation import ApplicationValidation

class ClientAlreadyExists(ApplicationValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="CLIENT_ALREADY_EXISTS",
        )
