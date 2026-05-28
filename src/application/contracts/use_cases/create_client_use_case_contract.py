from abc import ABC, abstractmethod
from src.application.use_cases.client.dtos.create_client_request_dto import CreateClientRequestDto
from src.application.use_cases.client.dtos.create_client_response_dto import CreateClientResponseDto

class CreateClientUseCaseContract(ABC):

    @abstractmethod
    async def execute(self,create_client_request_dto: CreateClientRequestDto) -> CreateClientResponseDto:
        pass
