from typing import Protocol

from domain.entities.client_entity import ClientEntity
from application.contracts.client_repository_contract import ClientRepositoryContract
from ..exceptions.fail_persist_on_database import FailPersistOnDatabase
from ..exceptions.fail_search_on_database import FailSearchOnDatabase
from .mappers.client_repository_mapper import ClientRepositoryMapper


class ClientDelegate(Protocol):
    async def create(self,data: dict) -> object:
        pass

    async def find_unique(self,where: dict) -> object | None:
        pass


class PrismaDatabase(Protocol):
    client: ClientDelegate


class ClientRepository(ClientRepositoryContract):
    def __init__(self,db: PrismaDatabase) -> None:
        self.db = db

    async def save(self,client_entity: ClientEntity) -> object:
        try:
            record = await self.db.client.create(
                data={
                    "client_id": str(client_entity.client_id),
                    "name": client_entity.name.value,
                    "email": client_entity.email.value,
                    "type_request": client_entity.type_request.value,
                    "asset_value": client_entity.asset_value.value,
                    "status": client_entity.status.value,
                    "priority": client_entity.priority.value,
                }
            )

            return ClientRepositoryMapper.to_public(record)

        except Exception as error:
            raise FailPersistOnDatabase(
                message="Failed to save client",
                external_error=error)

    async def find_by_email(self,email: str) -> ClientEntity | None:
        try:
            record = await self.db.client.find_unique(
                where={
                    "email": email,
                }
            )
            if record is None:
                return None

            return ClientRepositoryMapper.to_domain(record)

        except Exception as error:
            raise FailSearchOnDatabase(
                message="Failed to search client by email",
                external_error=error)
