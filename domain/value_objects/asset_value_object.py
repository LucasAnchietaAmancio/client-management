from decimal import Decimal

from domain.exceptions.type_mismatch import TypeMismatch
from domain.exceptions.asset_value_not_accept import AssetValueNotAccept

class AssetValueObject:
    def __init__(self,value: int | Decimal) -> None:

        if not isinstance(value,(int,Decimal)):
            raise TypeMismatch("Asset value must be an integer or Decimal")

        decimal_value = Decimal(value)

        if decimal_value <= 0:
            raise AssetValueNotAccept("Asset value cannot be negative or zero")

        self.value = decimal_value
