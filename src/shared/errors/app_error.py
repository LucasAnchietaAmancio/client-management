from typing import Any

class AppError(Exception):
    def __init__(self,tag: str,category: str,message: str,external_error: Exception | Any = None) -> None:
        self.tag = tag
        self.category = category
        self.message = message
        self.external_error = external_error
        super().__init__(self.message)
