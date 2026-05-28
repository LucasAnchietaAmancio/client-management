from typing import Any

from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.domain.entities.client_entity import ClientEntity
from src.infra.gateways.pipefy.utils.build_mutation_util import BuildMutationUtil

class PipefyGraphQLClient(PipefyGatewayContract):
    def __init__(self,http_provider: Any) -> None:
        self.http_provider = http_provider

    async def create_card(self,client_entity: ClientEntity) -> None:
        mutation = BuildMutationUtil.create_mutation(
            pipe_id=self.http_provider.pipe_id,
            title=client_entity.client_name.value,
            client_entity=client_entity,
        )
        await self.http_provider.post(mutation)

    async def update_card_fields(self,card_id: str,status: str,priority: str) -> None:
        mutation = BuildMutationUtil.update_mutation(
            card_id=card_id,
            status=status,
            priority=priority,
        )
        await self.http_provider.post(mutation)
