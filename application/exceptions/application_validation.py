
class ApplicationValidation(Exception):
    def __init__(self,message: str,tag: str = "APPLICATION_VALIDATION") -> None:
        self.tag = tag
        self.category = "APPLICATION"
        self.type = "VALIDATION"
        self.message = message
        super().__init__(self.message)
