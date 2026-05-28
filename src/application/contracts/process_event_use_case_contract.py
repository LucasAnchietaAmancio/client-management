from abc import ABC, abstractmethod

from src.application.use_cases.event.dtos.process_pipefy_webhook_request_dto import (ProcessPipefyWebhookRequestDto)
from src.application.use_cases.event.dtos.process_pipefy_webhook_response_dto import (ProcessPipefyWebhookResponseDto)

class ProcessEventUseCaseContract(ABC):

    @abstractmethod
    async def execute(self,process_pipefy_webhook_request_dto: ProcessPipefyWebhookRequestDto) -> ProcessPipefyWebhookResponseDto:
        pass
