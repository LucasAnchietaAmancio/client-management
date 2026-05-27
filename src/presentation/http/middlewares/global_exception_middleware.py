from typing import Any

from src.shared.errors.app_error import AppError


class GlobalExceptionMiddleware:

    type_to_status = {
        "VALIDATION": 400,
        "INPUT": 400,
        "UNAUTHORIZED": 401,
        "UNAUTHENTICATION": 401,
        "FORBIDDEN": 403,
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "RATE_LIMITED": 429,
        "INTERNAL": 500,
        "UNAVAILABLE": 503,
    }

    def __init__(self,app: Any,json_response: Any,status: Any,request_validation_error: type[Exception]) -> None:
        self.app = app
        self.json_response = json_response
        self.status = status
        self.request_validation_error = request_validation_error

    def register(self) -> None:
        self.app.add_exception_handler(
            self.request_validation_error,
            self.handle_request_validation_error,
        )
        self.app.add_exception_handler(
            AppError,
            self.handle_app_error,
        )
        self.app.add_exception_handler(
            Exception,
            self.handle_unhandled_error,
        )

    async def handle_request_validation_error(self,request: Any,error: Exception) -> Any:
        app_error = AppError(
            message="Invalid request body",
            code="INVALID_REQUEST_BODY",
            category="PRESENTATION",
            error_type="VALIDATION",
        )

        return self._build_error_response(app_error)

    async def handle_app_error(self,request: Any,error: AppError) -> Any:
        self._log_service_error(request,error)
        return self._build_error_response(error)

    async def handle_unhandled_error(self,request: Any,error: Exception) -> Any:
        print(f"\n[UNHANDLED ERROR] {request.method} {request.url.path}")
        print(error)
        print("---------------------------\n")

        return self.json_response(
            status_code=self.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected internal server error",
                    "category": "INTERNAL",
                    "type": "INTERNAL",
                },
            },
        )

    def _build_error_response(self,error: AppError) -> Any:
        status_code = self.type_to_status.get(error.type,self.status.HTTP_500_INTERNAL_SERVER_ERROR)

        return self.json_response(
            status_code=status_code,
            content={
                "success": False,
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "category": error.category,
                    "type": error.type,
                },
            },
        )

    def _log_service_error(self,request: Any,error: AppError) -> None:
        print(f"\n[SERVICE ERROR] {request.method} {request.url.path}")
        print(f"|-- Type: {error.type}")
        print(f"|-- Code: {error.code}")
        print(f"|-- Message: {error.message}")
        print("---------------------------\n")
