from src.application.contracts.process_event_use_case_contract import ProcessEventUseCaseContract
from src.application.use_cases.event.process_event_use_case import ProcessEventUseCase
from src.main.factories.repositories.client.client_repository_factory import make_client_repository
from src.main.factories.repositories.event.event_repository_factory import make_event_repository

def make_process_event_use_case() -> ProcessEventUseCaseContract:
    event_repository = make_event_repository()
    client_repository = make_client_repository()
    return ProcessEventUseCase(event_repository,client_repository)
