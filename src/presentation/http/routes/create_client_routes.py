from typing import Any, Callable

from src.presentation.http.controllers.create_client_controller import CreateClientController
from ..schema.create_client_schema import CreateClientRequestSchema


class CreateClientRoute:
    def __init__(
        self,
        router: Any,
        depends: Callable[..., Any],
        controller_factory: Callable[[], CreateClientController],
        created_status_code: int,
    ) -> None:
        self.router = router
        self.depends = depends
        self.controller_factory = controller_factory
        self.created_status_code = created_status_code

    def register(self) -> Any:
        controller_dependency = self.depends(self.controller_factory)

        @self.router.post("/clientes", status_code=self.created_status_code)
        async def handle(
            request: CreateClientRequestSchema,
            controller: CreateClientController = controller_dependency,
        ) -> dict[str, object]:
            return await controller.handle(request)

        return self.router
