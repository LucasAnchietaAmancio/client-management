# Client Management com Pipefy

Este documento descreve o fluxo atual implementado no projeto.

## Fluxo 1: Criacao de Cliente

### Entrada

`POST /clientes` com:

- `cliente_nome`
- `cliente_email`
- `tipo_solicitacao`
- `valor_patrimonio`

Tambem sao aceitos os campos normalizados:

- `client_name`
- `client_email`
- `type_request`
- `asset_value`

### Passo a passo

1. O cliente chama `POST /clientes`.
2. O controller valida o schema Pydantic.
3. O controller converte o payload em `CreateClientRequestDto`.
4. O use case cria a `ClientEntity`.
5. A entidade cria seus value objects e define:
   - `status = Aguardando Analise`
   - `priority = null`
6. O use case verifica se o email ja existe.
7. Se existir, dispara `ClientAlreadyExists`.
8. Se nao existir, salva no repositorio local.
9. O use case chama o gateway Pipefy.
10. O gateway monta a mutation `createCard`.
11. Em modo real, o provider HTTP envia o GraphQL para o Pipefy.
12. Em modo `development`, o mock imprime a mutation no console.

## Fluxo 2: Webhook de Atualizacao

### Entrada

`POST /webhooks/pipefy/card-updated` com:

- `event_id`
- `card_id`
- `cliente_email`
- `timestamp`

### Passo a passo

1. O Pipefy envia o webhook para a API.
2. O controller valida o schema.
3. O controller converte o payload em `ProcessPipefyWebhookRequestDto`.
4. O use case verifica se `event_id` ja foi processado.
5. Se o evento ja existir, dispara `EventAlreadyProcessed`.
6. Se nao existir, busca o cliente por email.
7. Se o cliente nao existir, dispara `NotExistClientForEvent`.
8. O use case chama `client.process()`.
9. O dominio calcula a prioridade:
   - `>= 200000` -> `prioridade_alta`
   - `< 200000` -> `prioridade_normal`
10. O use case chama o gateway Pipefy.
11. O gateway monta a mutation `updateCardField`.
12. O cliente e atualizado localmente para `Processado`.
13. O evento e salvo no repositorio para garantir idempotencia.

## Camadas

- `presentation`: controllers, schemas e rotas.
- `application`: use cases, DTOs e contratos.
- `domain`: entidades, enums, value objects e excecoes.
- `infra`: Prisma, mappers e integracao Pipefy.
- `main`: factories e composicao da aplicacao.

## Decisoes de implementacao

- O projeto usa nomes internos em ingles.
- A API aceita os campos em portugues por alias no Pydantic.
- O Pipefy real pode ser usado quando `PIPEFY_MODE` nao esta em `development`.
- O mock pode ser usado para demo local e para o recrutador rodar sem dependencia externa.
