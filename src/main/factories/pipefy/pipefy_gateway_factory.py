import os
import httpx

from src.application.contracts.gateways.pipefy_gateway_contract import PipefyGatewayContract
from src.infra.gateways.pipefy.client.pipefy_graphql_client import PipefyGraphQLClient
from src.infra.gateways.pipefy.pipefy_http_provider import PipefyHttpProvider
from src.infra.gateways.pipefy.mock.mock_pipefy_gateway import MockPipefyGateway

def make_pipefy_gateway() -> PipefyGatewayContract:

    if os.getenv("PIPEFY_MODE") == "development":
        return MockPipefyGateway()

    http_provider = PipefyHttpProvider(
        http=httpx,
        api_url=os.getenv("PIPEFY_API_URL"),
        token=os.getenv("PIPEFY_TOKEN"),
        pipe_id=os.getenv("PIPEFY_CLIENT_MANAGEMENT_PIPE_ID"),
    )
    return PipefyGraphQLClient(http_provider)
