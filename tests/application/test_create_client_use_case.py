import unittest

from application.contracts.client_repository_contract import ClientRepositoryContract
from application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto
from application.use_cases.client.create_client_use_case import CreateClientUseCase
from domain.entities.client_entity import ClientEntity


class InMemoryClientRepository(ClientRepositoryContract):
    def __init__(self) -> None:
        self.clients: list[ClientEntity] = []

    async def save(self,client_entity: ClientEntity) -> ClientEntity:
        self.clients.append(client_entity)
        return client_entity

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
                name="Joao Silva",
                email="joao.silva@example.com",
                type_request="Atualizacao cadastral",
                asset_value=250000,
            )
        )

        self.assertEqual(len(repository.clients),1)
        self.assertIsInstance(response,CreateClientResponseDto)
        self.assertEqual(response.name,"Joao Silva")
        self.assertEqual(response.email,"joao.silva@example.com")
        self.assertEqual(response.type_request,"Atualizacao cadastral")
        self.assertEqual(response.asset_value,250000)

if __name__ == "__main__":
    unittest.main()
