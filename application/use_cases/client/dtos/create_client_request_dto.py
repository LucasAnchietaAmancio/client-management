from dataclasses import dataclass


@dataclass(frozen=True)
class CreateClientRequestDto:
    name: str
    email: str
    type_request: str
    asset_value: int
