from src.application.contracts.use_cases.create_client_use_case_contract import CreateClientUseCaseContract
from src.application.use_cases.client.create_client_use_case import CreateClientUseCase
from src.main.factories.pipefy.pipefy_gateway_factory import make_pipefy_gateway
from src.main.factories.repositories.client.client_repository_factory import make_client_repository

def make_create_client_use_case() -> CreateClientUseCaseContract:
    client_repository = make_client_repository()
    pipefy_gateway = make_pipefy_gateway()
    return CreateClientUseCase(client_repository,pipefy_gateway)
