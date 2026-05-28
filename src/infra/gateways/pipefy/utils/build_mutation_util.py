import json
from typing import Any
from src.domain.entities.client_entity import ClientEntity

class BuildMutationUtil:

    @staticmethod
    def create_mutation(pipe_id: str,title: str,client_entity: ClientEntity) -> dict[str, Any]:
        return {
        "query": f"""
            mutation {{
              createCard(input: {{
                pipe_id: {pipe_id},
                title: {json.dumps(title)},
                fields_attributes: [
                  {{
                    field_id: "cliente_nome"
                    field_value: {json.dumps(client_entity.client_name.value)}
                  }},
                  {{
                    field_id: "cliente_email"
                    field_value: {json.dumps(client_entity.client_email.value)}
                  }},
                  {{
                    field_id: "tipo_solicitacao"
                    field_value: {json.dumps(client_entity.type_request.value)}
                  }},
                  {{
                    field_id: "valor_patrimonio"
                    field_value: {json.dumps(str(client_entity.asset_value.value))}
                  }}
                ]
              }}) {{
                card {{
                  id
                }}
              }}
            }}
            """.strip()
                }

    @staticmethod
    def update_mutation(card_id: str,status: str,priority: str) -> dict[str, Any]:
        return {
        "query": f"""
            mutation {{
              updateStatus: updateCardField(input: {{
                card_id: {json.dumps(card_id)}
                field_id: "status_cliente"
                new_value: {json.dumps(status)}
              }}) {{
                success
              }}
              updatePriority: updateCardField(input: {{
                card_id: {json.dumps(card_id)}
                field_id: "prioridade_cliente"
                new_value: {json.dumps(priority)}
              }}) {{
                success
              }}
            }}
            """.strip()
                }
