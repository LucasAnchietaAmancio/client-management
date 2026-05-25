
class DomainValidationError(Exception):
    def __init__(self,message: str,tag: str = "DOMAIN_VALIDATION_ERROR") -> None:
        self.tag = tag
        self.category = "DOMAIN"
        self.type = "VALIDATION"
        self.message = message
        super().__init__(self.message)
