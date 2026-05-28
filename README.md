# Client Management & Pipefy Integration

Projeto desenvolvido para o teste tecnico de Backend do fluxo de Client Management. O projeto usa uma conta Pipefy ja existente no ambiente de desenvolvimento para validar o fluxo de ponta a ponta, mantendo a mesma estrutura de mutations GraphQL exigida no teste.

Embora o enunciado fale simular o Pipefy localmente, optei por uma validacao real no ambiente de desenvolvimento para demonstrar o fluxo completo entre API, banco local e Pipefy. A aplicacao tambem suporta modo mock para execucao local sem integracao externa.

A aplicacao gerencia clientes, patrimonio investido e processamento de eventos de card. A persistencia local e feita em PostgreSQL via Docker, usando Prisma Client Python.

## Decisao de nomenclatura

O enunciado usa campos em portugues, como `cliente_nome`, `tipo_solicitacao` e `valor_patrimonio`.

Neste projeto, o codigo interno usa nomes em ingles (`client_name`, `type_request`, `asset_value`) para manter a pratica de desenvolvimento em ingles, comum em times e projetos internacionais. Mesmo assim, a API aceita normalmente o payload oficial em portugues por meio de aliases de validacao no Pydantic.

Na entrada, os dois formatos sao aceitos:

- Portugues: formato oficial do desafio.
- Ingles: formato normalizado usado internamente no projeto.

As respostas da API usam os nomes normalizados em ingles.

## Fluxos

### 1. Criacao de cliente

Endpoint:

```http
POST /clientes
```

Payload oficial aceito:

```json
{
  "cliente_nome": "Joao Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualizacao cadastral",
  "valor_patrimonio": 250000
}
```

Payload normalizado tambem aceito:

```json
{
  "client_name": "Joao Silva",
  "client_email": "joao.silva@example.com",
  "type_request": "Atualizacao cadastral",
  "asset_value": 250000
}
```

Comportamento:

- Valida campos obrigatorios.
- Valida formato de email na camada de dominio.
- Valida `asset_value`/`valor_patrimonio` como inteiro estrito.
- Cria o cliente com status inicial `Aguardando Analise`.
- Salva o cliente no banco local.
- Mantem a prioridade inicial como `null`, pois ela so e calculada no webhook.
- Envia a mutation `createCard` para o Pipefy no modo real, ou imprime a mutation no modo mock.

### 2. Webhook de atualizacao de card

Endpoint:

```http
POST /webhooks/pipefy/card-updated
```

Payload oficial aceito:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

Payload normalizado tambem aceito:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "client_email": "joao.silva@example.com",
  "timestamp": "2026-05-18T12:00:00Z"
}
```

Comportamento:

- Verifica idempotencia pelo `event_id`.
- Busca o cliente pelo email.
- Processa o cliente por metodo de dominio.
- Atualiza o status para `Processado`.
- Calcula a prioridade:
  - patrimonio maior ou igual a `200000`: `prioridade_alta`
  - patrimonio menor que `200000`: `prioridade_normal`
- Persiste o evento processado.
- Atualiza o cliente no banco local.
- Envia a mutation `updateCardField` para o Pipefy no modo real, ou imprime a mutation no modo mock.

## Pipefy GraphQL

A camada Pipefy monta mutations GraphQL reais e envia para o endpoint configurado no ambiente.

Para executar sem chamar o Pipefy real, use `PIPEFY_MODE=development`. Nesse modo a aplicacao usa `MockPipefyGateway` e imprime a mutation no console. Na aplicacao real, o provider HTTP faz `POST` em `PIPEFY_API_URL`.

As mutations GraphQL reais ficam estruturadas em:

```text
src/infra/pipefy/utils/build_mutation_util.py
```

O envio HTTP fica em:

```text
src/infra/pipefy/pipefy_http_provider.py
```

A documentacao oficial indica:

- `createCard`: cria um card em um pipe e recebe `input` com `pipe_id`, `fields_attributes` e opcionalmente `title`.
- `fields_attributes`: lista de campos com `field_id` e `field_value`.
- `updateCardField`: atualiza um campo do card e recebe `input` com `card_id`, `field_id` e `new_value`.

Referencias oficiais:

- https://developers.pipefy.com/reference/create-a-card-with-the-required-fields-fulfilled
- https://api-docs.pipefy.com/reference/inputObjects/CreateCardInput/
- https://api-docs.pipefy.com/reference/mutations/updateCardField/
- https://api-docs.pipefy.com/reference/inputObjects/UpdateCardFieldInput/

## Arquitetura

O projeto segue DDD + Clean Architecture:

- `src/domain`: entidades, value objects, enums e excecoes de dominio.
- `src/application`: casos de uso, DTOs e contratos.
- `src/infra`: Prisma, repositorios concretos, mappers e excecoes de infraestrutura.
- `src/presentation`: schemas, controllers, routes e middleware HTTP.
- `src/main`: composicao da aplicacao e factories.
- `main.py`: ponto de entrada FastAPI.

Regras aplicadas:

- Dominio nao importa FastAPI, Prisma ou infraestrutura.
- Use cases recebem DTOs e retornam DTOs.
- Controllers recebem schemas Pydantic, criam DTOs de entrada e retornam JSON.
- Repositorios concretos retornam `None` em comandos de escrita.
- Erros semanticamente conhecidos herdam diretamente de `AppError`.
- Middleware global padroniza erros da aplicacao e erros de schema.

## Requisitos

- Python 3.13
- Docker
- PostgreSQL via `docker-compose`

## Passo a passo completo

### 1. Copiar Repositorio
Copie o repositório:

```bash
git clone https://github.com/LucasAnchietaAmancio/client-management.git
```

## 2. Variaveis de ambiente

Crie um arquivo `.env` na raiz com base no .env.exemple

`PIPEFY_MODE=development` usa o `MockPipefyGateway` e evita chamadas reais ao Pipefy. Se a variavel estiver ausente ou diferente disso, a aplicacao usa a integracao real ou seja caso queira usar a integração real é só fazer `PIPEFY_MODE=` e subir o container.

### 3. Preparar o Pipefy

Antes de subir a API, configure no Pipefy o pipe que vai representar os clientes do sistema.

Anote os valores reais de:

- `PIPEFY_CLIENT_MANAGEMENT_PIPE_ID`
- o `field_id` dos campos usados no `createCard`
- o `field_id` dos campos usados no `updateCardField`

Neste projeto, esses IDs sao montados em `src/infra/pipefy/utils/build_mutation_util.py`. Se o seu pipe tiver IDs diferentes, ajuste esse arquivo para refletir a configuracao real do ambiente.

Se voce quiser apenas validar o projeto localmente sem enviar nada ao Pipefy, deixe `PIPEFY_MODE=development`.

### 4. Subir a aplicacao via Docker

Suba o projeto para validar:

```bash
docker compose up --build
```

### 5. Acessar a API

Documentacao interativa:

```text
http://localhost:8000/docs
```

### 6. Criar o card no Pipefy pelo endpoint de cliente

O card e criado quando voce chama o endpoint de cadastro:

```http
POST /clientes
```

Exemplo:

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

Nesse momento:

- o cliente e validado
- o cliente e salvo no banco local
- a mutation `createCard` e enviada ao Pipefy pelo provider HTTP
- a resposta do Pipefy e exibida no log do processo ou no console do mock

### 7. Simular o webhook de atualizacao do card

Depois que o card existe, simule a alteracao do card pelo endpoint de webhook:

```http
POST /webhooks/pipefy/card-updated
```

Exemplo:

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

Nesse momento:

- o `event_id` garante idempotencia
- o cliente e localizado pelo email
- a prioridade e calculada com base no patrimonio
- o status local vai para `Processado`
- a mutation `updateCardField` e enviada ao Pipefy pelo provider HTTP

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

Resposta esperada:

```json
{
  "client_name": "Joao Silva",
  "client_email": "joao.silva@example.com",
  "type_request": "Atualizacao cadastral",
  "asset_value": 250000
}
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

Resposta esperada:

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "client_email": "joao.silva@example.com",
  "status": "Processado",
  "priority": "prioridade_alta"
}
```

## Testes

Execute:

```bash
docker compose exec app python -m unittest
```

Coberturas principais:

- Criacao de cliente com payload valido e salvamento no repositorio.
- Processamento de webhook com `prioridade_alta`.
- Processamento de webhook com `prioridade_normal`.
- Bloqueio de webhook duplicado por `event_id`.
- Validacoes de dominio e value objects.
- Erros de infraestrutura em repositorios.
- Montagem das mutations GraphQL do Pipefy.
- Envio HTTP do provider Pipefy.

## CI

O projeto ja inclui uma pipeline de integracao continua em `.github/workflows/continuos_integration.yml`.

A pipeline atual executa:

- checkout do repositorio
- setup do Python 3.13
- instalacao das dependencias
- execucao dos testes com `python -m unittest`

## Visao de producao na AWS

Uma versao produtiva alinhada com o meu conhecimento atual pode ser uma aplicacao containerizada e distribuida em AWS da seguinte forma:

- A aplicacao e empacotada em uma imagem Docker.
- A imagem e publicada no Amazon ECR.
- O deploy e executado no Amazon ECS.
- O banco relacional continua em Amazon RDS PostgreSQL.
- Os segredos de integracao com Pipefy e banco ficam em AWS Secrets Manager.
- O deploy e automatizado com uma pipeline de CD integrada ao ECR e ao ECS.
- Os logs e metricas vao para CloudWatch.

## Status atual

Implementado:

- Dominio de cliente e evento.
- Use cases de criacao de cliente e processamento de webhook.
- Repositorios Prisma.
- Mappers dominio/persistencia.
- Client Pipefy GraphQL com envio HTTP real via provider e mutations `createCard` e `updateCardField`.
- Mock PipefyGateway para execucao local sem integracao externa.
- Controllers, schemas, routes e middleware global.
- FastAPI configurado em `main.py`.
- Docker Compose para PostgreSQL.
- Testes automatizados principais.
