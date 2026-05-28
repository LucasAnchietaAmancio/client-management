from typing import Any
from ..presentation.http.middlewares.global_exception_middleware import GlobalExceptionMiddleware
from src.main.factories.controllers.client.create_client_controller_factory import make_create_client_controller
from src.main.factories.controllers.event.process_event_controller_factory import make_process_event_controller
from src.presentation.http.routes.client.create_client_route import CreateClientRoute
from src.presentation.http.routes.event.process_event_route import ProcessEventRoute

class App:
    def __init__(self,app: Any,router: Any,depends: Any,status: Any,prisma_client: Any,json_response: Any,request_validation_error: type[Exception]) -> None:
        self.app = app
        self.router = router
        self.depends = depends
        self.status = status
        self.prisma_client = prisma_client
        self.json_response = json_response
        self.request_validation_error = request_validation_error

    def setup(self) -> Any:
        error_middleware = GlobalExceptionMiddleware(
            json_response=self.json_response,
            status=self.status,
            request_validation_error=self.request_validation_error,
        )
        self.app.middleware("http")(error_middleware.execute)
        self.app.add_exception_handler(self.request_validation_error,error_middleware.handle_request_validation_error)

        @self.app.on_event("startup")
        async def startup() -> None:
            await self.prisma_client.connect()

        @self.app.on_event("shutdown")
        async def shutdown() -> None:
            await self.prisma_client.disconnect()

        create_client_route = CreateClientRoute(
            router=self.router,
            depends=self.depends,
            controller_factory=make_create_client_controller,
            created_status_code=self.status.HTTP_201_CREATED,
        )
        process_event_route = ProcessEventRoute(
            router=self.router,
            depends=self.depends,
            controller_factory=make_process_event_controller,
            created_status_code=self.status.HTTP_200_OK,
        )

        create_client_route.register()
        process_event_route.register()
        self.app.include_router(self.router)

        return self.app
