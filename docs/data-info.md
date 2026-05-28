# Dados e Contratos

Este documento resume os dados que trafegam no projeto na versao atual.

O sistema segue DDD + Clean Architecture:

- `domain` concentra regras puras.
- `application` orquestra os casos de uso.
- `infra` implementa Prisma, mappers e a integracao Pipefy.
- `presentation` valida HTTP, converte para DTOs e retorna JSON.

## Fluxo 1: Criacao de Cliente

### Endpoint

```http
POST /clientes
```

### Payload aceito

Os dois formatos sao aceitos pela API:

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

```json
{
  "client_name": "Joao Silva",
  "client_email": "joao.silva@example.com",
  "type_request": "Atualizacao cadastral",
  "asset_value": 250000
}
```

### Saida de dominio

- `status` inicial: `Aguardando Analise`
- `priority` inicial: `null`

### Pipefy GraphQL

A camada de infra monta a mutation `createCard` em `src/infra/pipefy/utils/build_mutation_util.py`.

Campos usados no card:

- `cliente_nome`
- `cliente_email`
- `tipo_solicitacao`
- `valor_patrimonio`

## Fluxo 2: Webhook de Atualizacao

### Endpoint

```http
POST /webhooks/pipefy/card-updated
```

### Payload aceito

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

### Regra de negocio

- `valor_patrimonio >= 200000` -> `prioridade_alta`
- `valor_patrimonio < 200000` -> `prioridade_normal`

### Saida de dominio

- `status` final: `Processado`
- `priority` final: calculada pela regra acima

### Pipefy GraphQL

A camada de infra monta a mutation `updateCardField` para refletir o status e a prioridade do card.

## Tipos Principais

- `CreateClientRequestSchema`
- `ProcessEventSchema`
- `CreateClientRequestDto`
- `ProcessPipefyWebhookRequestDto`
- `ClientEntity`
- `EventEntity`

## Observacoes

- O webhook usa `event_id` para idempotencia.
- O `card_id` vem no payload do webhook.
- O projeto aceita modo `PIPEFY_MODE=development` para usar mock sem chamada real.
- O projeto aceita modo real quando `PIPEFY_MODE` nao esta em `development`.
