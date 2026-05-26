
class InfraValidation(Exception):
    def __init__(self,message: str,tag: str = "INFRASTRUCTURE_VALIDATION",external_error: Exception | None = None) -> None:
        self.tag = tag
        self.category = "INFRASTRUCTURE"
        self.type = "VALIDATION"
        self.message = message
        self.external_error = external_error
        super().__init__(self.message)
