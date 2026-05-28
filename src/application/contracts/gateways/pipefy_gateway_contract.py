from abc import ABC, abstractmethod
from src.domain.entities.client_entity import ClientEntity

class PipefyGatewayContract(ABC):

    @abstractmethod
    async def create_card(self,client_entity: ClientEntity) -> None:
        pass

    @abstractmethod
    async def update_card_fields(self,card_id: str,status: str,priority: str) -> None:
        pass
