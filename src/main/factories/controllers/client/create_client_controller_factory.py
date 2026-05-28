from src.main.factories.use_cases.client.create_client_use_case_factory import make_create_client_use_case
from src.presentation.http.controllers.client.create_client_controller import CreateClientController

def make_create_client_controller() -> CreateClientController:
    create_client_use_case = make_create_client_use_case()
    return CreateClientController(create_client_use_case)
