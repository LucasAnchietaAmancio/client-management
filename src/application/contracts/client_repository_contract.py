from abc import ABC, abstractmethod

from src.domain.entities.client_entity import ClientEntity

class ClientRepositoryContract(ABC):

    @abstractmethod
    async def save(self,client_entity: ClientEntity) -> dict[str, object]:
        pass

    @abstractmethod
    async def find_by_email(self,email: str) -> ClientEntity | None:
        pass

    @abstractmethod
    async def update(self,client_entity: ClientEntity) -> dict[str, object]:
        pass
