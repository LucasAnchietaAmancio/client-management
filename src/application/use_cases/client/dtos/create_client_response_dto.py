from dataclasses import dataclass

@dataclass(frozen=True)
class CreateClientResponseDto:
    client_name: str
    client_email: str
    type_request: str
    asset_value: int
