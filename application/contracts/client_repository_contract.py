from abc import ABC, abstractmethod

from domain.entities.client_entity import ClientEntity


class ClientRepositoryContract(ABC):

    @abstractmethod
    async def save(self,client_entity: ClientEntity) -> ClientEntity:
        pass

    @abstractmethod
    async def find_by_email(self,email: str) -> ClientEntity | None:
        pass
