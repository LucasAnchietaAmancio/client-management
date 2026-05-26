from .application_validation import ApplicationValidation

class NotExistClientForEvent(ApplicationValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="NOT_EXIST_CLIENT_FOR_EVENT",
        )
