from src.application.contracts.process_event_use_case_contract import ProcessEventUseCaseContract

from src.application.use_cases.event.dtos.process_pipefy_webhook_request_dto import ProcessPipefyWebhookRequestDto
from src.presentation.http.schema.event.process_event_schema import ProcessEventSchema

class ProcessEventController:
    def __init__(self, process_event_use_case: ProcessEventUseCaseContract):
        self.process_event_use_case = process_event_use_case

    async def handle(self, request: ProcessEventSchema) -> dict[str, object]:
        process_event_request_dto = ProcessPipefyWebhookRequestDto(
            event_id=request.event_id,
            card_id=request.card_id,
            client_email=request.client_email,
            timestamp=request.timestamp,
        )

        response = await self.process_event_use_case.execute(process_event_request_dto)

        return {
            "event_id": response.event_id,
            "card_id": response.card_id,
            "client_email": response.client_email,
            "status": response.status,
            "priority": response.priority,
        }
