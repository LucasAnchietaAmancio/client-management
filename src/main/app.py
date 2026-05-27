from typing import Any

from ..presentation.http.routes.create_client_routes import CreateClientRoute
from .factories.controllers.create_client_controller_factory import make_create_client_controller


class App:
    def __init__(self, app: Any, router: Any, depends: Any, status: Any) -> None:
        self.app = app
        self.router = router
        self.depends = depends
        self.status = status

    def setup(self) -> Any:
        create_client_route = CreateClientRoute(
            router=self.router,
            depends=self.depends,
            controller_factory=make_create_client_controller,
            created_status_code=self.status.HTTP_201_CREATED,
        )

        self.app.include_router(create_client_route.register())

        return self.app
