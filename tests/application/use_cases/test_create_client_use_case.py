import unittest

from src.application.contracts.client_repository_contract import ClientRepositoryContract
from src.application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from src.application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto
from src.application.use_cases.client.create_client_use_case import CreateClientUseCase
from src.domain.entities.client_entity import ClientEntity


class InMemoryClientRepository(ClientRepositoryContract):
    def __init__(self) -> None:
        self.clients: list[ClientEntity] = []

    async def save(self,client_entity: ClientEntity) -> None:
        self.clients.append(client_entity)

    async def find_by_client_email(self,client_email: str) -> ClientEntity | None:
        for client in self.clients:
            if client.client_email.value == client_email:
                return client

        return None

    async def update_by_id(self,client_entity: ClientEntity) -> None:
        return None


class TestCreateClientUseCase(unittest.IsolatedAsyncioTestCase):
    async def test_create_client_with_valid_input(self):
        repository = InMemoryClientRepository()
        use_case = CreateClientUseCase(repository)

        response = await use_case.execute(
            CreateClientRequestDto(
                client_name="Lucas",
                client_email="lucas@email.com",
                type_request="Atualizacao cadastral",
                asset_value=250000,
            )
        )

        self.assertEqual(len(repository.clients),1)
        self.assertIsInstance(response,CreateClientResponseDto)
        self.assertEqual(response.client_name,"Lucas")
        self.assertEqual(response.client_email,"lucas@email.com")
        self.assertEqual(response.type_request,"Atualizacao cadastral")
        self.assertEqual(response.asset_value,250000)

if __name__ == "__main__":
    unittest.main()
