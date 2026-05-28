import unittest

from src.application.contracts.repositories.client_repository_contract import ClientRepositoryContract
from src.application.contracts.repositories.event_repository_contract import EventRepositoryContract
from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.application.exceptions.event_already_processed import EventAlreadyProcessed
from src.application.exceptions.not_exist_client_for_event import NotExistClientForEvent
from src.application.use_cases.event.dtos.process_pipefy_webhook_request_dto import ProcessPipefyWebhookRequestDto
from src.application.use_cases.event.dtos.process_pipefy_webhook_response_dto import ProcessPipefyWebhookResponseDto
from src.application.use_cases.event.process_event_use_case import ProcessEventUseCase
from src.domain.entities.client_entity import ClientEntity
from src.domain.entities.event_entity import EventEntity


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


class InMemoryEventRepository(EventRepositoryContract):
    def __init__(self) -> None:
        self.events: list[EventEntity] = []

    async def save(self,event_entity: EventEntity) -> None:
        self.events.append(event_entity)

    async def find_by_id(self,event_id: str) -> EventEntity | None:
        for event in self.events:
            if event.event_id == event_id:
                return event

        return None


class InMemoryPipefyGateway(PipefyGatewayContract):
    def __init__(self) -> None:
        self.created_card_client: ClientEntity | None = None
        self.updated_card: dict[str, str] | None = None

    async def create_card(self,client_entity: ClientEntity) -> None:
        self.created_card_client = client_entity

    async def update_card_fields(self,card_id: str,status: str,priority: str) -> None:
        self.updated_card = {
            "card_id": card_id,
            "status": status,
            "priority": priority,
        }


class TestProcessEventUseCase(unittest.IsolatedAsyncioTestCase):
    async def test_process_event_updates_client_and_saves_event(self):
        client_repository = InMemoryClientRepository()
        event_repository = InMemoryEventRepository()
        pipefy_gateway = InMemoryPipefyGateway()
        use_case = ProcessEventUseCase(event_repository,client_repository,pipefy_gateway)
        client_repository.clients.append(
            ClientEntity.create(
                client_name="Lucas",
                client_email="lucas@email.com",
                type_request="Atualizacao cadastral",
                asset_value=250000,
            )
        )

        response = await use_case.execute(
            ProcessPipefyWebhookRequestDto(
                event_id="evt_123",
                card_id="card_456",
                client_email="lucas@email.com",
                timestamp="2026-05-18T12:00:00Z",
            )
        )

        self.assertIsInstance(response,ProcessPipefyWebhookResponseDto)
        self.assertEqual(response.status,"Processado")
        self.assertEqual(response.priority,"prioridade_alta")
        self.assertEqual(len(event_repository.events),1)
        self.assertEqual(pipefy_gateway.updated_card["card_id"],"card_456")
        self.assertEqual(pipefy_gateway.updated_card["status"],"Processado")
        self.assertEqual(pipefy_gateway.updated_card["priority"],"prioridade_alta")

    async def test_process_event_applies_normal_priority_when_asset_value_is_less_than_200000(self):
        client_repository = InMemoryClientRepository()
        event_repository = InMemoryEventRepository()
        pipefy_gateway = InMemoryPipefyGateway()
        use_case = ProcessEventUseCase(event_repository,client_repository,pipefy_gateway)
        client_repository.clients.append(
            ClientEntity.create(
                client_name="Lucas",
                client_email="lucas@email.com",
                type_request="Atualizacao cadastral",
                asset_value=150000,
            )
        )

        response = await use_case.execute(
            ProcessPipefyWebhookRequestDto(
                event_id="evt_124",
                card_id="card_456",
                client_email="lucas@email.com",
                timestamp="2026-05-18T12:00:00Z",
            )
        )

        self.assertEqual(response.status,"Processado")
        self.assertEqual(response.priority,"prioridade_normal")
        self.assertEqual(len(event_repository.events),1)
        self.assertEqual(pipefy_gateway.updated_card["priority"],"prioridade_normal")

    async def test_process_event_raises_when_event_already_processed(self):
        client_repository = InMemoryClientRepository()
        event_repository = InMemoryEventRepository()
        pipefy_gateway = InMemoryPipefyGateway()
        use_case = ProcessEventUseCase(event_repository,client_repository,pipefy_gateway)
        event_repository.events.append(
            EventEntity.create(
                event_id="evt_123",
                card_id="card_456",
                client_email="lucas@email.com",
                timestamp="2026-05-18T12:00:00Z",
            )
        )

        with self.assertRaises(EventAlreadyProcessed):
            await use_case.execute(
                ProcessPipefyWebhookRequestDto(
                    event_id="evt_123",
                    card_id="card_456",
                    client_email="lucas@email.com",
                    timestamp="2026-05-18T12:00:00Z",
                )
            )

    async def test_process_event_raises_when_client_does_not_exist(self):
        client_repository = InMemoryClientRepository()
        event_repository = InMemoryEventRepository()
        pipefy_gateway = InMemoryPipefyGateway()
        use_case = ProcessEventUseCase(event_repository,client_repository,pipefy_gateway)

        with self.assertRaises(NotExistClientForEvent):
            await use_case.execute(
                ProcessPipefyWebhookRequestDto(
                    event_id="evt_123",
                    card_id="card_456",
                    client_email="lucas@email.com",
                    timestamp="2026-05-18T12:00:00Z",
                )
            )


if __name__ == "__main__":
    unittest.main()
