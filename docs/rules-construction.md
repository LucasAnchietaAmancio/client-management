# Regras de Construção

Este documento resume as regras aplicadas na versao atual do projeto.

## Presentation

- Recebe requests HTTP.
- Valida payload com Pydantic.
- Converte request em DTO.
- Retorna JSON.
- Nao conhece banco, Prisma ou Pipefy.

## Application

- Orquestra os casos de uso.
- Recebe DTOs.
- Usa contratos de repositorio e gateway.
- Nao cria regra de negocio de forma direta.

## Domain

- Guarda regras puras.
- Usa entities, value objects e enums.
- `ClientEntity.create()` cria novos clientes.
- `ClientEntity.restore()` reconstrui registros do banco.
- `client.process()` altera status e prioridade.

## Infra

- Implementa Prisma.
- Implementa mappers entre dominio e persistencia.
- Implementa integracao Pipefy.
- Trata falhas externas com excecoes de infraestrutura.

## Pipefy

- `BuildMutationUtil` monta as mutations GraphQL.
- `PipefyHttpProvider` envia a requisicao HTTP real.
- `MockPipefyGateway` evita chamada externa no modo `development`.

## Erros

- Erros semanticamente conhecidos herdam diretamente de `AppError`.
- `AppError` carrega `tag`, `category`, `message` e `external_error`.
- `GlobalExceptionMiddleware` transforma erro em resposta JSON padronizada.

## Convencoes

- Use cases retornam DTOs.
- Repositorios de escrita retornam `None`.
- A API aceita payload em portugues e em ingles.
- O projeto usa `PIPEFY_MODE=development` para mock local.
