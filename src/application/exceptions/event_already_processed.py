from .application_validation import ApplicationValidation

class EventAlreadyProcessed(ApplicationValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="EVENT_ALREADY_PROCESSED",
            error_type="CONFLICT",
        )
