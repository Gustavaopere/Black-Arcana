# Localized Forbidden Domain

## Estado

`IMPLEMENTADO / VALIDAÇÃO FINAL DEFERIDA`

## Identidade

- **Domínio:** Forbidden Domains
- **Função:** campo localizado de realidade/regra

## Descrição

Cria uma arena/campo mágico bounded dentro de uma dimensão já carregada. O runtime atual fornece lifecycle, participant capture e authority de segurança, mas não inventa efeitos específicos de Blood/Soul/Arsenal sem provider/contrato aprovado.

## Hard ceilings confirmados

- **Raio máximo absoluto:** `24 blocos`.
- **Duração máxima absoluta:** `1.200 ticks`.
- **Participantes/entidades rastreados:** `64` por domínio.
- **Domínios ativos:** `8` server-wide.
- **Domínios ativos por owner:** `1`.
- **Budget de metadata/restauração:** `512 posições`.

## Segurança

- sem dimensão temporária;
- sem force-loading;
- sem clone de inventory/capability/player state;
- sem arbitrary terrain mutation no runtime base;
- loaded chunks, border, protection, world-effect e safe-recovery são authority canônica;
- cleanup por expiry, owner logout/death/unavailable e server stop;
- close exactly-once/idempotent.

## Dano / efeitos específicos

`FAIL-CLOSED` por padrão. O runtime não atribui automaticamente dano, blood, soul ou arsenal effects.

## Custo / cooldown / aprendizado

`TBD — Stage 08 / spell/provider específico que hospedar o domínio`.

## Uso futuro em Caos/Ordem

Pode servir como infraestrutura compartilhada para campos de realidade do Caos e campos de lei/selamento da Ordem, desde que os efeitos específicos sejam implementados sem enfraquecer D032.
