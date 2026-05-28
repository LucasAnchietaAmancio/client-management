from src.application.contracts.create_client_use_case_contract import CreateClientUseCaseContract

from src.application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from src.presentation.http.schema.client.create_client_schema import CreateClientRequestSchema

class CreateClientController:
    def __init__(self, create_client_use_case: CreateClientUseCaseContract) -> None:
        self.create_client_use_case = create_client_use_case

    async def handle(self, request: CreateClientRequestSchema) -> dict[str, object]:
        create_client_request_dto = CreateClientRequestDto(
            client_name=request.client_name,
            client_email=request.client_email,
            type_request=request.type_request,
            asset_value=request.asset_value,
        )

        response = await self.create_client_use_case.execute(create_client_request_dto)

        return {
            "client_name": response.client_name,
            "client_email": response.client_email,
            "type_request": response.type_request,
            "asset_value": response.asset_value,
        }
