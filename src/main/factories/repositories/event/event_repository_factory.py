from src.infra.database.repositories.event.event_repository import EventRepository
from src.main.factories.database.prisma_client_factory import make_prisma_client

def make_event_repository() -> EventRepository:
    db = make_prisma_client().get_client()
    return EventRepository(db)
