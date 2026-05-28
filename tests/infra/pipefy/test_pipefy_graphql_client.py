import unittest

from src.domain.entities.client_entity import ClientEntity
from src.infra.gateways.pipefy.client.pipefy_graphql_client import PipefyGraphQLClient


class FakeHttpProvider:
    def __init__(self) -> None:
        self.pipe_id = "34"
        self.sent_payloads: list[dict] = []

    async def post(self,payload: dict) -> None:
        self.sent_payloads.append(payload)


class TestPipefyGraphQLClient(unittest.IsolatedAsyncioTestCase):
    async def test_create_card_sends_create_card_mutation_to_http_provider(self):
        http_provider = FakeHttpProvider()
        pipefy_client = PipefyGraphQLClient(http_provider)
        client = ClientEntity.create(
            client_name="Lucas",
            client_email="lucas@email.com",
            type_request="Atualizacao cadastral",
            asset_value=250000,
        )

        await pipefy_client.create_card(client)
        payload = http_provider.sent_payloads[0]

        self.assertIn("createCard",payload["query"])
        self.assertIn("pipe_id: 34",payload["query"])
        self.assertIn('title: "Lucas"',payload["query"])
        self.assertIn('field_id: "cliente_nome"',payload["query"])
        self.assertIn('field_value: "Lucas"',payload["query"])
        self.assertIn('field_id: "cliente_email"',payload["query"])
        self.assertIn('field_value: "lucas@email.com"',payload["query"])
        self.assertIn('field_id: "tipo_solicitacao"',payload["query"])
        self.assertIn('field_value: "Atualizacao cadastral"',payload["query"])
        self.assertIn('field_id: "valor_patrimonio"',payload["query"])
        self.assertIn('field_value: "250000"',payload["query"])

    async def test_update_card_fields_sends_update_card_field_mutation_to_http_provider(self):
        http_provider = FakeHttpProvider()
        pipefy_client = PipefyGraphQLClient(http_provider)

        await pipefy_client.update_card_fields(
            card_id="card_456",
            status="Processado",
            priority="prioridade_alta",
        )
        payload = http_provider.sent_payloads[0]

        self.assertIn("updateCardField",payload["query"])
        self.assertIn('card_id: "card_456"',payload["query"])
        self.assertIn('field_id: "status_cliente"',payload["query"])
        self.assertIn('new_value: "Processado"',payload["query"])
        self.assertIn('field_id: "prioridade_cliente"',payload["query"])
        self.assertIn('new_value: "prioridade_alta"',payload["query"])


if __name__ == "__main__":
    unittest.main()
