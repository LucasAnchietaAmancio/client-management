from typing import Any

from src.shared.errors.app_error import AppError

class GlobalExceptionMiddleware:

    category_to_status = {
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

    def __init__(self,json_response: Any,status: Any,request_validation_error: type[Exception]) -> None:
        self.json_response = json_response
        self.status = status
        self.request_validation_error = request_validation_error

    async def execute(self,request: Any, call_next: Any) -> Any:
        try:
            response = await call_next(request)
            return response

        except Exception as err:
            if isinstance(err, AppError):
                return self.json_response(
                    status_code= self.category_to_status[err.category],
                    content= {
                        "success": False,
                        "error": {
                            "tag": err.tag,
                            "message": err.message,
                            "metadata": {
                                "category": err.category,
                                "cause": str(err.external_error) if err.external_error else None,
                            }
                        }
                    }
                )

            return self.json_response(
                status_code= 500,
                content={
                    "success": False,
                    "error": {
                        "tag": "INTERNAL_SERVER_ERROR",
                        "message": "Internal Server Error",
                        "metadata": {
                            "category": "INTERNAL",
                            "cause": str(err)
                        },
                    }
                }
            )

    async def handle_request_validation_error(self,request: Any, err: Exception) -> Any:
        return self.json_response(
            status_code= 422,
            content={
                "success": False,
                "error": {
                    "tag": "INVALID_SCHEMA",
                    "message": "Schema invalid for this request",
                    "metadata": {
                        "category": "UNPROCESSABLE_ENTITY",
                        "cause": err.errors()
                    }
                }
            }
        )
