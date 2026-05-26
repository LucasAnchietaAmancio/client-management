from src.domain.exceptions.type_mismatch import TypeMismatch
from src.domain.exceptions.asset_value_not_accept import AssetValueNotAccept

class AssetValueObject:
    def __init__(self,value: int) -> None:

        if isinstance(value,bool) or not isinstance(value,int):
            raise TypeMismatch("Asset value must be an integer")

        if value <= 0:
            raise AssetValueNotAccept("Asset value cannot be negative or zero")

        self.value = value
