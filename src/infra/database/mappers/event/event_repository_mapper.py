from src.domain.entities.event_entity import EventEntity

class EventRepositoryMapper:

    @staticmethod
    def to_domain(record: object)-> EventEntity:
        return EventEntity.restore(
            event_id= record.event_id,
            card_id= record.card_id,
            client_email= record.client_email,
            timestamp= record.timestamp
        )

    @staticmethod
    def to_persistence(event_entity: EventEntity) -> dict:
        return {
            "event_id": event_entity.event_id,
            "card_id": event_entity.card_id,
            "client_email": event_entity.client_email.value,
            "timestamp": event_entity.timestamp,
        }
