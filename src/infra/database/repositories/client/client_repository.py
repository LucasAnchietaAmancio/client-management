from typing import Any
from src.application.contracts.repositories.client_repository_contract import ClientRepositoryContract
from src.domain.entities.client_entity import ClientEntity
from src.infra.database.mappers.client.client_repository_mapper import ClientRepositoryMapper
from src.infra.exceptions.fail_persist_on_database import FailPersistOnDatabase
from src.infra.exceptions.fail_search_on_database import FailSearchOnDatabase
from src.infra.exceptions.fail_update_on_database import FailUpdateOnDatabase

class ClientRepository(ClientRepositoryContract):
    def __init__(self,db: Any) -> None:
        self.db = db

    async def save(self,client_entity: ClientEntity) -> None:
        try:
            await self.db.client.create(
                data= ClientRepositoryMapper.to_persistence(client_entity)
            )
            
        except Exception as error:
            raise FailPersistOnDatabase(
                message="Failed to save use_cases",
                external_error=error)

    async def find_by_client_email(self,client_email: str) -> ClientEntity | None:
        try:
            record = await self.db.client.find_unique(
                where={
                    "client_email": client_email,
                }
            )
            if record is None:
                return None

            return ClientRepositoryMapper.to_domain(record)

        except Exception as error:
            raise FailSearchOnDatabase(
                message="Failed to search use_cases by client_email",
                external_error=error)

    async def update_by_id(self,client_entity: ClientEntity) -> None:
        try:
            update_data = ClientRepositoryMapper.to_persistence(client_entity)
            update_data.pop("client_id", None)

            await self.db.client.update(
                where={
                    "client_id": str(client_entity.client_id),
                },
                data=update_data
            )

        except Exception as error:
            raise FailUpdateOnDatabase(
                message="Failed to update use_cases",
                external_error=error
            )
