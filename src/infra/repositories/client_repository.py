from src.domain.entities.client_entity import ClientEntity
from src.application.contracts.client_repository_contract import ClientRepositoryContract
from ..exceptions.fail_persist_on_database import FailPersistOnDatabase
from ..exceptions.fail_search_on_database import FailSearchOnDatabase
from .mappers.client_repository_mapper import ClientRepositoryMapper

class ClientRepository(ClientRepositoryContract):
    def __init__(self,db: "PrismaClient") -> None:
        self.db = db

    async def save(self,client_entity: ClientEntity) -> dict[str, object]:
        try:
            record = await self.db.client.create(
                data= ClientRepositoryMapper.to_persistence(client_entity)
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

    async def update(self,client_entity: ClientEntity) -> dict[str, object]:
        return ClientRepositoryMapper.to_public(
            type("ClientRecord",(),ClientRepositoryMapper.to_persistence(client_entity))()
        )
