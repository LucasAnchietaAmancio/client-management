from src.application.contracts.repositories.client_repository_contract import ClientRepositoryContract
from src.application.contracts.repositories.event_repository_contract import EventRepositoryContract
from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.application.contracts.use_cases.process_event_use_case_contract import ProcessEventUseCaseContract
from src.application.exceptions.event_already_processed import EventAlreadyProcessed
from src.application.exceptions.not_exist_client_for_event import NotExistClientForEvent
from src.application.use_cases.event.dtos.process_pipefy_webhook_request_dto import ProcessPipefyWebhookRequestDto
from src.application.use_cases.event.dtos.process_pipefy_webhook_response_dto import ProcessPipefyWebhookResponseDto
from src.domain.entities.event_entity import EventEntity

class ProcessEventUseCase(ProcessEventUseCaseContract):
    
    def __init__(self,event_repository: EventRepositoryContract,client_repository: ClientRepositoryContract,pipefy_gateway: PipefyGatewayContract) -> None:
        self.event_repository = event_repository
        self.client_repository = client_repository
        self.pipefy_gateway = pipefy_gateway

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

        client_from_event = await self.client_repository.find_by_client_email(event.client_email.value)

        if client_from_event is None:
            raise NotExistClientForEvent("Not exist use_cases for event sended")

        client_from_event.process()

        await self.pipefy_gateway.update_card_fields(
            card_id=event.card_id,
            status=client_from_event.status.value,
            priority=client_from_event.priority.value,
        )
        await self.event_repository.save(event)
        await self.client_repository.update_by_id(client_from_event)

        return ProcessPipefyWebhookResponseDto(
            event_id=event.event_id,
            card_id=event.card_id,
            client_email=event.client_email.value,
            status=client_from_event.status.value,
            priority=client_from_event.priority.value,
        )
