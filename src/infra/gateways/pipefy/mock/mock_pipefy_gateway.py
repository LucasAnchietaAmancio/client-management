from typing import Any

from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.domain.entities.client_entity import ClientEntity
from src.infra.gateways.pipefy.utils.build_mutation_util import BuildMutationUtil

class MockPipefyGateway(PipefyGatewayContract):
    def __init__(self) -> None:
        self.create_card_payload: Any = None
        self.update_card_payload: Any = None

    async def create_card(self,client_entity: ClientEntity) -> None:
        self.create_card_payload = BuildMutationUtil.create_mutation(
            pipe_id="mock-pipe-id",
            title=client_entity.client_name.value,
            client_entity=client_entity,
        )
        print("Created card in pipefy gateway on mode test")
        print(self.create_card_payload["query"])

    async def update_card_fields(self,card_id: str,status: str,priority: str) -> None:
        self.update_card_payload = BuildMutationUtil.update_mutation(
            card_id=card_id,
            status=status,
            priority=priority,
        )
        print("Updated card in pipefy gateway on mode test")
        print(self.update_card_payload["query"])
