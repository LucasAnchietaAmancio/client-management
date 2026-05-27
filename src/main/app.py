from typing import Any

from ..presentation.http.middlewares.global_exception_middleware import GlobalExceptionMiddleware
from routes.client.create_client_routes import CreateClientRoute
from .factories.controllers.create_client_controller_factory import make_create_client_controller

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
        GlobalExceptionMiddleware(
            app=self.app,
            json_response=self.json_response,
            status=self.status,
            request_validation_error=self.request_validation_error,
        ).register()

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

        self.app.include_router(create_client_route.register())

        return self.app
