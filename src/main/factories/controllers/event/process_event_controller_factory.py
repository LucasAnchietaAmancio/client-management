from src.main.factories.use_cases.event.process_event_use_case_factory import make_process_event_use_case
from src.presentation.http.controllers.event.process_event_controller import ProcessEventController

def make_process_event_controller() -> ProcessEventController:
    process_event_use_case = make_process_event_use_case()
    return ProcessEventController(process_event_use_case)
