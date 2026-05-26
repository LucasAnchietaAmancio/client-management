import unittest

from application.contracts.client_repository_contract import ClientRepositoryContract
from application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto
from application.use_cases.client.create_client_use_case import CreateClientUseCase
from domain.entities.client_entity import ClientEntity


class InMemoryClientRepository(ClientRepositoryContract):
    def __init__(self) -> None:
        self.clients: list[ClientEntity] = []

    async def save(self,client_entity: ClientEntity) -> object:
        self.clients.append(client_entity)
        return {
            "client_id": str(client_entity.client_id),
            "name": client_entity.name.value,
            "email": client_entity.email.value,
            "type_request": client_entity.type_request.value,
            "asset_value": client_entity.asset_value.value,
        }

    async def find_by_email(self,email: str) -> ClientEntity | None:
        for client in self.clients:
            if client.email.value == email:
                return client

        return None


class TestCreateClientUseCase(unittest.IsolatedAsyncioTestCase):
    async def test_create_client_with_valid_input(self):
        repository = InMemoryClientRepository()
        use_case = CreateClientUseCase(repository)

        response = await use_case.execute(
            CreateClientRequestDto(
                name="Lucas",
                email="lucas@email.com",
                type_request="Atualizacao cadastral",
                asset_value=250000,
            )
        )

        self.assertEqual(len(repository.clients),1)
        self.assertIsInstance(response,CreateClientResponseDto)
        self.assertEqual(response.name,"Lucas")
        self.assertEqual(response.email,"lucas@email.com")
        self.assertEqual(response.type_request,"Atualizacao cadastral")
        self.assertEqual(response.asset_value,250000)

if __name__ == "__main__":
    unittest.main()
