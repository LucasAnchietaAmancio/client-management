from abc import ABC, abstractmethod
from src.domain.entities.client_entity import ClientEntity

class ClientRepositoryContract(ABC):

    @abstractmethod
    async def save(self,client_entity: ClientEntity) -> None:
        pass

    @abstractmethod
    async def find_by_client_email(self,client_email: str) -> ClientEntity | None:
        pass

    @abstractmethod
    async def update_by_id(self,client_entity: ClientEntity) -> None:
        pass
