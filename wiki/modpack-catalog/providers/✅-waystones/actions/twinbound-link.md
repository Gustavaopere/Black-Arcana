# Twinbound Link

**Prova binária física (2026-10-13):** ✅ `COUNTED_EXACT` — `TwinboundFeatherItem.onUseTick → TwinboundFeatherLinksComponent.with` confirmado no JAR físico `21.1.45`; reciprocal cooperative link without teleport. [Java21 #38460510230](https://github.com/Gustavaopere/Black-Arcana/actions/runs/38460510230), [dossiê](../EXACT-BINARY-ACTIONS-21.1.45.md). Sem promoção de custo, multiplayer, persistência ou Survival (⚠️); +0 nova ação.

- Provider: **Waystones** (`waystones`)
- Version: `21.1.45`
- Classificação: **cooperative ritual-like supernatural action**
- Semantic state: `COUNTED_EXACT` (**identidade física estática somente**)
- Strict contribution: `1`
- Provider surface: **Twinbound Feather**

## Identidade semântica

Ação cooperativa independente em que dois jogadores usam Twinbound Feathers de forma sincronizada e mutuamente direcionada.

A conclusão persiste estado recíproco de vínculo provider-owned. Uma Feather vinculada pode então expor o parceiro como destination dinâmica no ecossistema Waystones.

## Deduplicação

Criar o vínculo não executa o teleport e não duplica a raiz **Waystone Warp / Teleport**. O vínculo prepara estado persistente de destino; o eventual transporte continua pertencendo ao pipeline normal do provider.

## Evidence boundary

A identidade, persistência causal e source-level reachability estão fechadas. Timing da interação, edge cases multiplayer, reconnect/persistence e policy de servidor permanecem QA de runtime.

Source: `../SOURCE-21.1.45-SEMANTIC-CLOSURE.md`.
