from typing import Any
from src.application.contracts.repositories.event_repository_contract import EventRepositoryContract
from src.domain.entities.event_entity import EventEntity
from src.infra.database.mappers.event.event_repository_mapper import EventRepositoryMapper
from src.infra.exceptions.fail_persist_on_database import FailPersistOnDatabase
from src.infra.exceptions.fail_search_on_database import FailSearchOnDatabase

class EventRepository(EventRepositoryContract):
    def __init__(self,db: Any) -> None:
        self.db = db

    async def save(self,event_entity: EventEntity) -> None:
        try:
            await self.db.event.create(
                data=EventRepositoryMapper.to_persistence(event_entity)
            )

        except Exception as error:
            raise FailPersistOnDatabase(
                message="Failed to save event",
                external_error=error)

    async def find_by_id(self,event_id: str) -> EventEntity | None:
        try:
            record = await self.db.event.find_unique(
                where={
                    "event_id": event_id,
                }
            )
            if record is None:
                return None

            return EventRepositoryMapper.to_domain(record)

        except Exception as error:
            raise FailSearchOnDatabase(
                message="Failed to search event by id",
                external_error=error)
