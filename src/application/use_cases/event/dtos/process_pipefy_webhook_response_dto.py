from dataclasses import dataclass

@dataclass(frozen=True)
class ProcessPipefyWebhookResponseDto:
    event_id: str
    card_id: str
    client_email: str
    status: str
    priority: str
