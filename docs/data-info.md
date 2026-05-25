# Dados Trafegados e Tipos

Este documento descreve os dados iniciais que trafegam pela API, pelos casos de uso e pela camada de integracao simulada com o Pipefy.

A modelagem considera uma arquitetura em Python seguindo DDD, SOLID e Clean Architecture, separando contratos de entrada, entidades de dominio, persistencia local e payloads GraphQL.

## Convencoes Gerais

- Datas e horarios devem trafegar em formato ISO 8601 com timezone, por exemplo `2026-05-18T12:00:00Z`.
- Valores monetarios devem ser tratados como `Decimal` no dominio para evitar perda de precisao.
- Emails devem ser normalizados antes da persistencia, preferencialmente em lowercase.
- Status e prioridade devem ser representados por enums ou value objects no dominio.
- IDs externos do Pipefy devem ser tratados como `str`, mesmo quando a API aceite identificadores numericos.

## Fluxo 1: Criacao de Cliente

### Endpoint

```http
POST /clientes
```

### Request Body

| Campo | Tipo JSON | Tipo Python sugerido | Obrigatorio | Origem/Camada | Descricao |
| --- | --- | --- | --- | --- | --- |
| `cliente_nome` | `string` | `str` | Sim | DTO de entrada | Nome completo do cliente. |
| `cliente_email` | `string` | `EmailStr` ou value object `Email` | Sim | DTO de entrada / dominio | Email usado como identificador de busca do cliente. |
| `tipo_solicitacao` | `string` | `str` ou enum `TipoSolicitacao` | Sim | DTO de entrada | Motivo que originou o card no Pipefy. |
| `valor_patrimonio` | `number` | `Decimal` | Sim | DTO de entrada / dominio | Valor do patrimonio investido do cliente. |

### Exemplo

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

### Dados Gerados pela Aplicacao

| Campo | Tipo Python sugerido | Camada | Descricao |
| --- | --- | --- | --- |
| `id` | `UUID` ou `int` | Infra / persistencia | Identificador local do cliente. |
| `status` | enum `ClienteStatus` | Dominio | Criado inicialmente como `Aguardando Analise`. |
| `prioridade` | enum `ClientePrioridade` ou `None` | Dominio | Nula na criacao; definida apos webhook. |
| `created_at` | `datetime` | Infra / persistencia | Data de criacao do registro local. |
| `updated_at` | `datetime` | Infra / persistencia | Data da ultima atualizacao local. |

### Entidade de Dominio: Cliente

| Atributo | Tipo Python sugerido | Regra |
| --- | --- | --- |
| `id` | `UUID` ou `int` | Pode ser gerado pela aplicacao ou pelo banco. |
| `nome` | `str` | Nao deve ser vazio. |
| `email` | value object `Email` | Deve ter formato valido. |
| `tipo_solicitacao` | `str` ou enum | Deve representar a solicitacao recebida. |
| `valor_patrimonio` | `Decimal` | Deve ser maior ou igual a zero. |
| `status` | enum `ClienteStatus` | Inicialmente `Aguardando Analise`. |
| `prioridade` | enum `ClientePrioridade` ou `None` | Definida no processamento do webhook. |

### Payload GraphQL Simulado: createCard

Este payload deve ficar isolado em um client/servico de infraestrutura, por exemplo `PipefyClient`, sem vazar detalhes de GraphQL para o dominio.

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `query` | `str` | String da mutation `createCard` conforme documentacao do Pipefy. |
| `variables.pipe_id` | `str` ou `int` | Identificador do pipe onde o card seria criado. |
| `variables.title` | `str` | Titulo do card, podendo usar o nome do cliente. |
| `variables.fields_attributes` | `list[dict]` | Lista de campos do card com nome, email, tipo de solicitacao e patrimonio. |

### Variaveis Esperadas para o Pipefy

| Variavel | Tipo Python sugerido | Origem |
| --- | --- | --- |
| `cliente_nome` | `str` | Request body / entidade `Cliente`. |
| `cliente_email` | `str` | Request body / value object `Email`. |
| `tipo_solicitacao` | `str` | Request body / entidade `Cliente`. |
| `valor_patrimonio` | `Decimal` | Request body / entidade `Cliente`. |

## Fluxo 2: Webhook de Atualizacao de Card

### Endpoint

```http
POST /webhooks/pipefy/card-updated
```

### Request Body

| Campo | Tipo JSON | Tipo Python sugerido | Obrigatorio | Origem/Camada | Descricao |
| --- | --- | --- | --- | --- | --- |
| `event_id` | `string` | `str` | Sim | DTO de entrada | Identificador unico do evento usado para idempotencia. |
| `card_id` | `string` | `str` | Sim | DTO de entrada | Identificador do card no Pipefy. |
| `cliente_email` | `string` | `EmailStr` ou value object `Email` | Sim | DTO de entrada / dominio | Email usado para localizar o cliente local. |
| `timestamp` | `string` | `datetime` | Sim | DTO de entrada | Momento em que o evento ocorreu no Pipefy. |

### Exemplo

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

### Registro de Idempotencia

| Campo | Tipo Python sugerido | Descricao |
| --- | --- | --- |
| `event_id` | `str` | Chave unica do evento processado. |
| `card_id` | `str` | Card relacionado ao evento. |
| `cliente_email` | `str` | Cliente relacionado ao evento. |
| `processed_at` | `datetime` | Momento em que o sistema processou o evento. |

### Regra de Prioridade

| Condicao | Prioridade resultante |
| --- | --- |
| `valor_patrimonio >= 200000` | `prioridade_alta` |
| `valor_patrimonio < 200000` | `prioridade_normal` |

### Atualizacao Local do Cliente

| Campo | Valor apos webhook | Tipo Python sugerido |
| --- | --- | --- |
| `status` | `Processado` | enum `ClienteStatus` |
| `prioridade` | `prioridade_alta` ou `prioridade_normal` | enum `ClientePrioridade` |
| `updated_at` | Data/hora atual | `datetime` |

### Payload GraphQL Simulado: updateCardField

Este payload tambem deve ficar na camada de infraestrutura, mantendo o caso de uso dependente apenas de uma interface, por exemplo `PipefyGateway`.

| Campo | Tipo | Descricao |
| --- | --- | --- |
| `query` | `str` | String da mutation de atualizacao de campo do card conforme documentacao do Pipefy. |
| `variables.card_id` | `str` | Identificador do card recebido no webhook. |
| `variables.field_id_status` | `str` | Identificador do campo de status no Pipefy. |
| `variables.field_id_prioridade` | `str` | Identificador do campo de prioridade no Pipefy. |
| `variables.status` | `str` | Valor `Processado`. |
| `variables.prioridade` | `str` | Valor calculado pela regra de negocio. |

### Variaveis Esperadas para o Pipefy

| Variavel | Tipo Python sugerido | Origem |
| --- | --- | --- |
| `card_id` | `str` | Webhook recebido. |
| `status` | `str` | Regra da aplicacao: `Processado`. |
| `prioridade` | `str` | Regra de negocio baseada em `valor_patrimonio`. |

## Contratos Internos por Camada

### Interface de Entrada

Responsavel por converter HTTP em DTOs de aplicacao.

| Contrato | Tipo sugerido | Responsabilidade |
| --- | --- | --- |
| `CreateClienteRequest` | Pydantic model | Validar payload de `POST /clientes`. |
| `PipefyCardUpdatedWebhookRequest` | Pydantic model | Validar payload do webhook. |

### Application

Responsavel por orquestrar casos de uso sem conhecer detalhes de framework, banco ou GraphQL.

| Caso de uso | Entrada | Saida esperada |
| --- | --- | --- |
| `CreateClienteUseCase` | `CreateClienteCommand` | Cliente criado e payload Pipefy simulado. |
| `ProcessPipefyWebhookUseCase` | `ProcessPipefyWebhookCommand` | Cliente processado, evento salvo e payload Pipefy simulado. |

### Domain

Responsavel pelas regras puras.

| Elemento | Tipo sugerido | Responsabilidade |
| --- | --- | --- |
| `Cliente` | Entity | Representar cliente e seu estado. |
| `Email` | Value Object | Garantir email valido e normalizado. |
| `ClienteStatus` | Enum | Controlar `Aguardando Analise` e `Processado`. |
| `ClientePrioridade` | Enum | Controlar `prioridade_alta` e `prioridade_normal`. |
| `calcular_prioridade` | Domain service ou metodo da entidade | Aplicar regra por patrimonio. |

### Infrastructure

Responsavel por detalhes externos.

| Componente | Tipo sugerido | Responsabilidade |
| --- | --- | --- |
| `ClienteRepository` | Interface no application/domain | Abstrair persistencia de clientes. |
| `SqlAlchemyClienteRepository` | Implementacao infra | Persistir clientes no banco local. |
| `WebhookEventRepository` | Interface | Abstrair idempotencia por `event_id`. |
| `SqlAlchemyWebhookEventRepository` | Implementacao infra | Salvar eventos processados. |
| `PipefyGateway` | Interface | Abstrair envio/simulacao de GraphQL. |
| `PipefyGraphQLClient` | Implementacao infra | Montar mutations `createCard` e `updateCardField`. |

## Tipos de Resposta Sugeridos

### POST /clientes

```json
{
  "id": "1",
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "status": "Aguardando Analise",
  "pipefy_simulation": {
    "operation": "createCard",
    "sent": false
  }
}
```

### POST /webhooks/pipefy/card-updated

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "prioridade_alta",
  "pipefy_simulation": {
    "operation": "updateCardField",
    "sent": false
  }
}
```

### Webhook Duplicado

```json
{
  "event_id": "evt_123",
  "status": "ignored",
  "reason": "Evento ja processado"
}
```

## Observacoes de Design

- O dominio nao deve depender de FastAPI, SQLAlchemy, Pydantic ou GraphQL.
- Os casos de uso devem depender de interfaces, nao de implementacoes concretas.
- O client do Pipefy deve apenas montar/simular os payloads GraphQL neste teste tecnico.
- As mutations reais devem ficar centralizadas para facilitar a demonstracao no video de defesa.
- A validacao de formato de entrada pode ficar nos DTOs, enquanto regras de negocio devem ficar no dominio.
