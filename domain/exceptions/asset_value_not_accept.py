from domain.exceptions.domain_validation_error import DomainValidationError

class AssetValueNotAccept(DomainValidationError):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="ASSET_VALUE_NOT_ACCEPT",
        )
