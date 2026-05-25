from domain.exceptions.type_mismatch import TypeMismatch
from domain.exceptions.empty_value import EmptyValue
from domain.exceptions.invalid_value import InvalidValue

class NameValueObject:
    def __init__(self,value: str) -> None:

        if not isinstance(value,str):
            raise TypeMismatch("Name must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise EmptyValue("Name cannot be empty")

        if len(normalized_value) < 3:
            raise InvalidValue("Name must have at least 3 characters")

        self.value = normalized_value
