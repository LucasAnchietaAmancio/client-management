from domain.value_objects.email_value_object import EmailValueObject

class EventEntity:
    def __init__(self,event_id: str,card_id: str,client_email: EmailValueObject,timestamp: str) -> None:
        self.event_id = event_id
        self.card_id = card_id
        self.client_email = client_email
        self.timestamp = timestamp

    @staticmethod
    def create(event_id: str,card_id: str,client_email: str,timestamp: str) -> "EventEntity":
        return EventEntity(
            event_id=event_id,
            card_id=card_id,
            client_email=EmailValueObject(client_email),
            timestamp=timestamp,
        )

    @staticmethod
    def restore(event_id: str,card_id: str,client_email: str,timestamp: str) -> "EventEntity":
        return EventEntity(
            event_id=event_id,
            card_id=card_id,
            client_email=EmailValueObject(client_email),
            timestamp=timestamp,
        )