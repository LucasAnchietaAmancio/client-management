from domain.exceptions.domain_validation import DomainValidation


class AssetValueNotAccept(DomainValidation):
    def __init__(self,message: str) -> None:
        super().__init__(
            message=message,
            tag="ASSET_VALUE_NOT_ACCEPT",
        )
