from abc import ABC, abstractmethod
from src.domain.entities.event_entity import EventEntity

class EventRepositoryContract(ABC):

    @abstractmethod
    async def save(self,event_entity: EventEntity) -> None:
        pass

    @abstractmethod
    async def find_by_id(self,event_id: str) -> EventEntity | None:
        pass
