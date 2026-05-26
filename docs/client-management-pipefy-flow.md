# Client Management com Pipefy — Documentação de Fluxo

---

## Fluxo 1: Criação de Cliente

### Entrada
`POST /clientes` com os campos:
- `cliente_nome`
- `cliente_email`
- `tipo_solicitacao`
- `valor_patrimonio`

### Passo a Passo

1. O usuário/sistema externo envia uma requisição `POST /clientes`.
2. O **Controller** recebe a requisição HTTP.
3. O Controller valida a estrutura básica do payload:
   - Verifica se o JSON é válido
   - Verifica se os campos obrigatórios foram enviados
   - Verifica tipos básicos esperados
4. O Controller transforma o payload em um `CreateClientRequestDto`.
5. O Controller chama o `CreateClientUseCase`.
6. O `CreateClientUseCase` cria uma `ClientEntity` usando `ClientEntity.create`.
7. A `ClientEntity` cria e valida seus Value Objects:
   - `NameValueObject` — valida nome
   - `EmailValueObject` — valida formato de e-mail
   - `TypeRequestValueObject` — valida tipo de solicitação
   - `AssetValueObject` — valida patrimônio como inteiro positivo
8. A `ClientEntity` nasce com:
   - `status = Aguardando Análise`
   - `prioridade = prioridade_nao_processada`
9. O `CreateClientUseCase` chama `ClientRepository.find_by_email` para verificar duplicidade.
10. **Se o e-mail já existir:**
    - O use case lança `ClientAlreadyExists`
    - O fluxo é encerrado com erro
11. **Se o e-mail não existir:**
    - O use case chama `ClientRepository.save`
12. O `ClientRepository` monta o objeto de persistência para o Prisma:
    - `client_id`, `name`, `email`, `type_request`, `asset_value`, `status`, `priority`
13. O `ClientRepository` salva o cliente no banco via Prisma.
14. **Se ocorrer erro ao salvar:**
    - O repository lança `FailPersistOnDatabase`
15. **Se salvar com sucesso:**
    - O repository retorna um objeto público via `ClientRepositoryMapper.to_public`
16. O `CreateClientUseCase` retorna o resultado para o Controller.
17. O Controller responde a requisição HTTP com os dados públicos do cliente criado.
18. *(Futuro)* Nesse fluxo, a camada Pipefy poderá montar a mutation GraphQL `createCard`.

---

## Fluxo 2: Webhook Pipefy — Card Updated

### Entrada
`POST /webhooks/pipefy/card-updated` com os campos:
- `event_id`
- `card_id`
- `cliente_email`
- `timestamp`

### Passo a Passo

1. O Pipefy/sistema externo envia `POST /webhooks/pipefy/card-updated`.
2. O **Controller** recebe a requisição HTTP.
3. O Controller valida a estrutura básica do payload (todos os campos obrigatórios).
4. O Controller transforma o payload em um `ProcessPipefyWebhookRequestDto`.
5. O Controller chama o `ProcessPipefyWebhookUseCase`.
6. O use case consulta `WebhookEventRepository.find_by_event_id` usando `event_id`.
7. **Se o `event_id` já existir (evento duplicado):**
   - O fluxo é encerrado como duplicado
   - O Controller retorna resposta informando evento ignorado
8. **Se o `event_id` não existir:**
   - O use case continua o processamento
9. O use case chama `ClientRepository.find_by_email` usando `cliente_email`.
10. **Se o cliente não for encontrado:**
    - O use case lança exceção `ClientNotFound`
    - O fluxo é encerrado com erro
11. **Se o cliente for encontrado:**
    - O repository retorna uma `ClientEntity` restaurada do banco
12. O use case chama `client.process()`.
13. A `ClientEntity` altera seu `status` para **Processado**.
14. A `ClientEntity` calcula a prioridade:
    - Se `valor_patrimonio >= 200000` → `prioridade_alta`
    - Se `valor_patrimonio < 200000` → `prioridade_normal`
15. O use case chama `ClientRepository.update` para salvar status e prioridade.
16. **Se ocorrer erro ao atualizar:**
    - O repository lança exceção de infraestrutura
17. O use case cria uma `WebhookEventEntity` com: `event_id`, `card_id`, `cliente_email`, `timestamp`.
18. O use case chama `WebhookEventRepository.save` para registrar o evento.
19. Esse registro garante **idempotência** para futuras chamadas com o mesmo `event_id`.
20. **Se ocorrer erro ao salvar o evento:**
    - O repository lança exceção de infraestrutura
21. *(Futuro)* Nesse fluxo, a camada Pipefy poderá montar a mutation GraphQL `updateCardField` com `status` e `prioridade`.
22. O use case retorna o resultado para o Controller.
23. O Controller responde com: `event_id`, `card_id`, `cliente_email`, `status = Processado`, prioridade calculada.

---

## Camadas Envolvidas

### Controller
- Recebe HTTP
- Valida estrutura básica do payload
- Converte payload em DTO
- Chama use case
- Retorna resposta HTTP

### Application / Use Cases
- Orquestra o fluxo
- Verifica duplicidade de cliente
- Verifica idempotência do webhook
- Chama repositories
- Não conhece detalhes do banco ou framework

### Domain
- Contém entidades e regras de negócio
- `ClientEntity` controla status e prioridade
- `WebhookEventEntity` representa eventos processados
- Value Objects validam dados individuais
- Enums representam status e prioridade

### Infra
- Implementa repositories
- Usa Prisma para persistir no banco
- Converte registros do banco para entidades
- Lança exceções específicas de infraestrutura
- *(Futuro)* Monta payloads GraphQL do Pipefy

---

## Principais Decisões de Design

| Decisão | Onde fica |
|---|---|
| Validação de estrutura | Controller |
| Validação de valor | Value Objects (Domain) |
| Regra de prioridade | `ClientEntity` (Domain) |
| Idempotência de webhook | `ProcessPipefyWebhookUseCase` + `WebhookEventRepository` |
| Acesso ao banco | Apenas camada de Infra |
| Dependência de contratos | Use cases dependem de interfaces, não de implementações concretas |
