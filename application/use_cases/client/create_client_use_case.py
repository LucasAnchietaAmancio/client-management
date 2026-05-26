from application.contracts.client_repository_contract import ClientRepositoryContract
from domain.entities.client_entity import ClientEntity
from application.exceptions.client_already_exists import ClientAlreadyExists
from application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto

class CreateClientUseCase:
    def __init__(self,client_repository: ClientRepositoryContract) -> None:
        self.client_repository = client_repository

    async def execute(self,create_client_request_dto: CreateClientRequestDto) -> CreateClientResponseDto:

        client = ClientEntity.create(
            name=create_client_request_dto.name,
            email=create_client_request_dto.email,
            type_request=create_client_request_dto.type_request,
            asset_value=create_client_request_dto.asset_value,
        )

        existing_client = await self.client_repository.find_by_email(client.email.value)

        if existing_client:
            raise ClientAlreadyExists("A customer already exists with that email address, please choose another email address")

        client_persisted_public = await self.client_repository.save(client)

        return CreateClientResponseDto(
            name=client_persisted_public["name"],
            email=client_persisted_public["email"],
            type_request=client_persisted_public["type_request"],
            asset_value=client_persisted_public["asset_value"],
        )
