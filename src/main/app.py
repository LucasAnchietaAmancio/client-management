from fastapi import APIRouter, Depends, FastAPI, status

from ..presentation.http.routes.create_client_routes import CreateClientRoute
from .factories.controllers.create_client_controller_factory import make_create_client_controller


class App:
    def __init__(self, app: FastAPI, router: APIRouter) -> None:
        self.app = app
        self.router = router

    def setup(self) -> FastAPI:
        create_client_route = CreateClientRoute(
            router=self.router,
            depends=Depends,
            controller_factory=make_create_client_controller,
            created_status_code=status.HTTP_201_CREATED,
        )

        self.app.include_router(create_client_route.register())

        return self.app


app = App(
    app=FastAPI(title="Client Management API"),
    router=APIRouter(),
).setup()
