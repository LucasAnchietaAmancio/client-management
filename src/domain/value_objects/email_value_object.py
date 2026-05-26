import re

from src.domain.exceptions.invalid_email import InvalidEmail
from src.domain.exceptions.type_mismatch import TypeMismatch

class EmailValueObject:
    EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self,value: str) -> None:

        if not isinstance(value, str):
            raise TypeMismatch("Email must be a string")

        normalized_value = value.strip().lower()

        if not self.EMAIL_REGEX.match(normalized_value):
            raise InvalidEmail("Invalid email, please insert a valid email address")

        self.value = normalized_value
