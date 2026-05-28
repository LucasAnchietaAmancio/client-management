from typing import Any
from src.infra.exceptions.fail_pipefy_request import FailPipefyRequest

class PipefyHttpProvider:
    def __init__(self,http: Any,api_url: str,token: str,pipe_id: str) -> None:
        self.http = http
        self.api_url = api_url
        self.token = token
        self.pipe_id = pipe_id

    async def post(self,payload: dict[str, Any]) -> None:
        if not self.token:
            raise FailPipefyRequest("Pipefy token is not configured")

        try:
            async with self.http.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json",
                    },
                )

            response.raise_for_status()
            response_data = response.json()

            if response_data.get("errors"):
                raise FailPipefyRequest(
                    message="Pipefy GraphQL returned errors",
                    external_error=response_data["errors"],
                )

        except FailPipefyRequest:
            raise
        except Exception as error:
            raise FailPipefyRequest(
                message="Failed to execute Pipefy GraphQL request",
                external_error=error,
            )
