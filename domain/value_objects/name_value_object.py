from domain.exceptions.type_mismatch import TypeMismatch
from domain.exceptions.empty_value_error import EmptyValueError
from domain.exceptions.invalid_value_error import InvalidValueError

class NameValueObject:
    def __init__(self,value: str) -> None:

        if not isinstance(value,str):
            raise TypeMismatch("Name must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise EmptyValueError("Name cannot be empty")

        if len(normalized_value) < 3:
            raise InvalidValueError("Name must have at least 3 characters")

        self.value = normalized_value
