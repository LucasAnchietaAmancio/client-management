from src.application.contracts.client_repository_contract import ClientRepositoryContract
from src.application.contracts.event_repository_contract import EventRepositoryContract
from src.application.exceptions.event_already_processed import EventAlreadyProcessed
from src.application.exceptions.not_exist_client_for_event import NotExistClientForEvent
from src.application.use_cases.webhook_event.dtos.process_pipefy_webhook_request_dto import ProcessPipefyWebhookRequestDto
from src.application.use_cases.webhook_event.dtos.process_pipefy_webhook_response_dto import ProcessPipefyWebhookResponseDto
from src.domain.entities.event_entity import EventEntity

class ProcessEventUseCase:
    def __init__(self,event_repository: EventRepositoryContract,client_repository: ClientRepositoryContract) -> None:
        self.event_repository = event_repository
        self.client_repository = client_repository

    async def execute(self,process_pipefy_webhook_request_dto: ProcessPipefyWebhookRequestDto) -> ProcessPipefyWebhookResponseDto:
        event = EventEntity.create(
            event_id=process_pipefy_webhook_request_dto.event_id,
            card_id=process_pipefy_webhook_request_dto.card_id,
            client_email=process_pipefy_webhook_request_dto.client_email,
            timestamp=process_pipefy_webhook_request_dto.timestamp,
        )

        event_already_processed = await self.event_repository.find_by_id(event.event_id)

        if event_already_processed:
            raise EventAlreadyProcessed("A event was already processed, please try again with new event_id")

        client_from_event = await self.client_repository.find_by_email(event.client_email.value)

        if client_from_event is None:
            raise NotExistClientForEvent("Not exist client for event sended")

        client_from_event.process()

        await self.client_repository.update(client_from_event)

        event_persisted_public = await self.event_repository.save(event)

        return ProcessPipefyWebhookResponseDto(
            event_id=event_persisted_public["event_id"],
            card_id=event_persisted_public["card_id"],
            client_email=event_persisted_public["client_email"],
            status=client_from_event.status.value,
            priority=client_from_event.priority.value,
        )
