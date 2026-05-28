from src.application.contracts.repositories.client_repository_contract import ClientRepositoryContract
from src.application.contracts.use_cases.create_client_use_case_contract import CreateClientUseCaseContract
from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.domain.entities.client_entity import ClientEntity
from src.application.exceptions.client_already_exists import ClientAlreadyExists
from src.application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from src.application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto

class CreateClientUseCase(CreateClientUseCaseContract):
    def __init__(self,client_repository: ClientRepositoryContract,pipefy_gateway: PipefyGatewayContract) -> None:
        self.client_repository = client_repository
        self.pipefy_gateway = pipefy_gateway

    async def execute(self,create_client_request_dto: CreateClientRequestDto) -> CreateClientResponseDto:

        client = ClientEntity.create(
            client_name=create_client_request_dto.client_name,
            client_email=create_client_request_dto.client_email,
            type_request=create_client_request_dto.type_request,
            asset_value=create_client_request_dto.asset_value,
        )

        existing_client = await self.client_repository.find_by_client_email(client.client_email.value)

        if existing_client:
            raise ClientAlreadyExists("A customer already exists with that email address, please choose another email address")

        await self.pipefy_gateway.create_card(client)
        await self.client_repository.save(client)

        return CreateClientResponseDto(
            client_name=client.client_name.value,
            client_email=client.client_email.value,
            type_request=client.type_request.value,
            asset_value=client.asset_value.value,
        )
