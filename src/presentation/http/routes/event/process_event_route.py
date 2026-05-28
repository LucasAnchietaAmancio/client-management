from typing import Any, Callable

from src.presentation.http.controllers.event.process_event_controller import ProcessEventController
from src.presentation.http.schema.event.process_event_schema import ProcessEventSchema

class ProcessEventRoute:
    def __init__(self,router: Any,depends: Callable[..., Any],controller_factory: Callable[[], ProcessEventController],created_status_code: int) -> None:
        self.router = router
        self.depends = depends
        self.controller_factory = controller_factory
        self.created_status_code = created_status_code

    def register(self) -> Any:
        controller_dependency = self.depends(self.controller_factory)

        @self.router.post("/webhooks/pipefy/card-updated", status_code=self.created_status_code)
        async def handle(request: ProcessEventSchema, controller: ProcessEventController = controller_dependency) -> dict[str, object]:
            return await controller.handle(request)

        return self.router
