class AppError(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        category: str,
        error_type: str,
    ) -> None:
        self.code = code
        self.tag = code
        self.category = category
        self.type = error_type
        self.message = message
        super().__init__(self.message)
