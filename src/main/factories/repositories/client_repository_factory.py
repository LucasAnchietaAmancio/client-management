from src.application.contracts.client_repository_contract import ClientRepositoryContract

def make_client_repository() -> ClientRepositoryContract:
    raise RuntimeError("ClientRepository dependency was not configured")
