from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessPipefyWebhookRequestDto:
    event_id: str
    card_id: str
    client_email: str
    timestamp: str
