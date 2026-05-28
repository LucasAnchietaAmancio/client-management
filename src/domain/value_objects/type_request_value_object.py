from src.domain.exceptions.empty_value import EmptyValue
from src.domain.exceptions.type_mismatch import TypeMismatch

class TypeRequestValueObject:
    def __init__(self,value: str) -> None:

        if not isinstance(value,str):
            raise TypeMismatch("Type request must be a string")

        normalized_value = value.strip()

        if not normalized_value:
            raise EmptyValue("Type request cannot be empty")

        self.value = normalized_value
