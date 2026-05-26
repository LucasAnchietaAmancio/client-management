# TESTE TECNICO: Desenvolvedor Backend

## Client Management & Pipefy Integration

Este repositorio foi criado como parte de um teste tecnico para a vaga de Desenvolvedor Backend.

O objetivo e desenvolver o esqueleto de um sistema interno para o Mundo Invest, responsavel por gerenciar clientes, seus patrimonios investidos e o mapeamento dessas acoes para o Pipefy.

Neste projeto, a integracao com o Pipefy deve ser simulada. A aplicacao deve persistir os dados em um banco local, mas as queries e mutations GraphQL estruturadas no codigo devem seguir o formato da documentacao oficial do Pipefy.

## Fluxos principais

### 1. Criacao de cliente

Endpoint previsto:

```http
POST /clientes
```

Payload esperado:

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

Responsabilidades:

- Validar campos obrigatorios.
- Validar formato de email.
- Persistir o cliente no banco local.
- Definir status inicial como `Aguardando Analise`.
- Estruturar a mutation GraphQL `createCard` para simular a criacao de card no Pipefy.

### 2. Webhook de atualizacao de card

Endpoint previsto:

```http
POST /webhooks/pipefy/card-updated
```

Payload esperado:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

Observacao: este payload e uma simulacao simplificada para o teste tecnico. Na documentacao oficial do Pipefy, o webhook de atualizacao de campo usa a action `card.field_update` e envia os dados dentro de `data`, incluindo `data.action`, `data.field`, `data.new_value`, `data.updated_by` e `data.card`.

Referencias oficiais:

- Pipefy Developers - Pipe & Table Webhooks: https://developers.pipefy.com/reference/pipe-table-webhooks
- Pipefy GraphQL API - Webhook object: https://api-docs.pipefy.com/reference/objects/Webhook/
- Pipefy Help Center - How to use webhooks: https://help.pipefy.com/en/articles/729719-how-to-use-webhooks-in-pipefy

Responsabilidades:

- Garantir idempotencia pelo `event_id`.
- Buscar cliente pelo email.
- Aplicar regra de prioridade com base no patrimonio.
- Estruturar mutation GraphQL para atualizar campos do card no Pipefy.
- Atualizar status do cliente para `Processado`.
- Salvar a prioridade calculada.

## Regras de negocio

- Patrimonio maior ou igual a `200000`: `prioridade_alta`.
- Patrimonio menor que `200000`: `prioridade_normal`.
- Status inicial do cliente: `Aguardando Analise`.
- Status apos processamento do webhook: `Processado`.
- Emails devem ter formato valido.
- Eventos de webhook duplicados nao devem ser processados novamente.

## Estrutura do projeto

```text
client-management/
├── docs/
│   ├── bussines-rule.md
│   ├── data-info.md
│   └── functional-and-not-functional-requeriments.md
├── src/
│   ├── application/
│   ├── domain/
│   ├── infra/
│   └── main/
├── main.py
└── README.md
```

## Camadas

- `domain`: entidades, value objects e regras de negocio.
- `application`: casos de uso da aplicacao.
- `infra`: banco de dados, repositorios e integracoes externas.
- `main`: configuracao da aplicacao e exposicao dos endpoints.
- `docs`: documentacao inicial do desafio e regras do sistema.

## Tecnologias previstas

- Python
- API REST
- FastAPI
- PostgreSQL via docker para ambiente produtivo
- GraphQL para mapeamento com Pipefy
- Testes automatizados

## Testes obrigatorios

O projeto deve conter testes automatizados cobrindo:

- Criacao de cliente com payload valido e salvamento no banco.
- Processamento de webhook aplicando a prioridade correta.
- Bloqueio de processamento duplicado pelo `event_id`.

## Execucao local

As instrucoes de execucao serao atualizadas conforme a API, banco e testes forem implementados.

## Exemplos de requisicao

### Criar cliente

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "Joao Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualizacao cadastral",
    "valor_patrimonio": 250000
  }'
```

### Simular webhook do Pipefy

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

## Status

Projeto em desenvolvimento inicial para entrega do teste tecnico.
