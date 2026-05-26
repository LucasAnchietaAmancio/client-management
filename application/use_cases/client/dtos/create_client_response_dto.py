from dataclasses import dataclass

@dataclass(frozen=True)
class CreateClientResponseDto:
    name: str
    email: str
    type_request: str
    asset_value: int
